"""Credits gems bought through RevenueCat to a user's Firestore wallet.

RevenueCat calls the webhook (see api/index.py) for every store event. We act on:

- NON_RENEWING_PURCHASE for a gem pack -> add its gems to the wallet
- CANCELLATION of a gem pack (a refund)  -> take those gems back

Each store transaction is recorded in Purchases/{store}_{transaction_id}, so
retried or duplicated webhooks never credit twice.

Wallet: Users/{uid}/wallet/main = { gems, unlocked, rewarded, createdAt }.
Firestore rules stop clients from adding gems; this server uses the Admin
SDK, which bypasses rules. Keep WELCOME_BONUS in sync with GemRules in
mobile/lib/features/wallet/models/wallet_model.dart and firestore.rules.
"""

from __future__ import annotations

import hashlib
import hmac
import re
import time
from dataclasses import dataclass
from typing import Any

from google.cloud import firestore

WELCOME_BONUS = 3
ANONYMOUS_PREFIX = "$RCAnonymousID:"
_GEMS_IN_PRODUCT = re.compile(r"gems_(\d+)")


def gems_for_product(product_id: str | None) -> int | None:
    """`dartic_gems_25` -> 25. Same rule as GemStoreService.gemsForProduct."""
    match = _GEMS_IN_PRODUCT.search(product_id or "")
    return int(match.group(1)) if match else None


def firebase_uid(event: dict[str, Any]) -> str | None:
    """The Firebase uid the app logged in to RevenueCat with, if any."""
    candidates = [
        event.get("app_user_id"),
        event.get("original_app_user_id"),
        *(event.get("aliases") or []),
    ]
    for candidate in candidates:
        if candidate and not str(candidate).startswith(ANONYMOUS_PREFIX):
            return str(candidate)
    return None


def valid_authorization(header: str | None, expected: str) -> bool:
    """RevenueCat sends the Authorization value set in its dashboard."""
    return bool(expected) and hmac.compare_digest(header or "", expected)


def valid_signature(header: str | None, raw_body: bytes, secret: str,
                    tolerance_s: int = 300, now: float | None = None) -> bool:
    """Checks X-RevenueCat-Webhook-Signature: t=<unix>,v1=<hex hmac-sha256>
    computed over "<t>.<raw body>" with the integration's signing secret."""
    try:
        parts = dict(item.split("=", 1) for item in (header or "").split(","))
        timestamp, signature = parts["t"], parts["v1"]
    except (KeyError, ValueError):
        return False
    if abs((now or time.time()) - int(timestamp)) > tolerance_s:
        return False
    expected = hmac.new(secret.encode(), f"{timestamp}.".encode() + raw_body,
                        hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


@dataclass
class Outcome:
    action: str  # credited | refunded | duplicate | ignored
    detail: str = ""
    gems: int = 0
    uid: str | None = None


def handle_event(db: firestore.Client, event: dict[str, Any]) -> Outcome:
    event_type = event.get("type")
    if event_type not in ("NON_RENEWING_PURCHASE", "CANCELLATION"):
        return Outcome("ignored", f"event type {event_type}")

    gems = gems_for_product(event.get("product_id"))
    if not gems:
        return Outcome("ignored", f"not a gem pack: {event.get('product_id')}")

    uid = firebase_uid(event)
    if uid is None:
        # The app logs users in before showing the store, so this means a
        # purchase made while signed out. Nothing to credit it to.
        return Outcome("ignored", "anonymous RevenueCat user")

    transaction_id = event.get("transaction_id") or event.get("id")
    purchase_ref = db.collection("Purchases").document(
        f"{event.get('store', 'store')}_{transaction_id}".replace("/", "_"))
    wallet_ref = db.collection("Users").document(uid).collection("wallet").document("main")

    if event_type == "NON_RENEWING_PURCHASE":
        return _credit(db.transaction(), purchase_ref, wallet_ref, event, uid, gems)
    return _refund(db.transaction(), db, purchase_ref, event)


@firestore.transactional
def _credit(tx, purchase_ref, wallet_ref, event, uid, gems) -> Outcome:
    if purchase_ref.get(transaction=tx).exists:
        return Outcome("duplicate", "already credited", gems, uid)
    wallet = wallet_ref.get(transaction=tx)

    tx.set(purchase_ref, {
        "uid": uid,
        "productId": event.get("product_id"),
        "gems": gems,
        "store": event.get("store"),
        "environment": event.get("environment"),
        "transactionId": event.get("transaction_id"),
        "eventId": event.get("id"),
        "purchasedAtMs": event.get("purchased_at_ms"),
        "status": "credited",
        "creditedAt": firestore.SERVER_TIMESTAMP,
    })
    if wallet.exists:
        tx.update(wallet_ref, {"gems": firestore.Increment(gems)})
    else:
        # Same shape the app creates, so later client updates pass the rules.
        tx.set(wallet_ref, {
            "gems": WELCOME_BONUS + gems,
            "unlocked": [],
            "rewarded": [],
            "createdAt": firestore.SERVER_TIMESTAMP,
        })
    return Outcome("credited", "", gems, uid)


@firestore.transactional
def _refund(tx, db, purchase_ref, event) -> Outcome:
    purchase = purchase_ref.get(transaction=tx)
    if not purchase.exists or purchase.get("status") != "credited":
        return Outcome("ignored", "no credited purchase to refund")
    # Take gems back from whoever was credited, even if the RevenueCat user
    # has since been aliased to another id.
    owner = purchase.get("uid")
    gems = int(purchase.get("gems"))
    wallet_ref = db.collection("Users").document(owner).collection("wallet").document("main")
    wallet = wallet_ref.get(transaction=tx)

    taken = min(gems, int(wallet.get("gems") or 0)) if wallet.exists else 0
    tx.update(purchase_ref, {
        "status": "refunded",
        "refundedAt": firestore.SERVER_TIMESTAMP,
        "cancelReason": event.get("cancel_reason"),
        "gemsTakenBack": taken,
    })
    if taken:
        # Never below zero: gems already spent on unlocks stay spent.
        tx.update(wallet_ref, {"gems": firestore.Increment(-taken)})
    return Outcome("refunded", "", taken, owner)
