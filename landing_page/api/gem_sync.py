"""Credits gem purchases by asking RevenueCat, triggered by the app.

Used instead of webhooks (which need a paid RevenueCat plan). After a
purchase, and whenever the wallet loads, the signed-in app calls
POST /api/gems/sync with its Firebase ID token. We then:

1. read the user's purchases from RevenueCat's REST API with the secret key
   (GET /v1/subscribers/{uid}; the app logs in to RevenueCat with its uid),
2. credit every gem-pack transaction not yet in Purchases/, using the same
   transaction-level dedupe as the webhook, so each purchase counts once.

The client only says "check me"; it never tells us what or how much it
bought, so it can't mint gems.

Refunds aren't detected here (RevenueCat's v1 customer response doesn't
reliably flag them). The webhook path handles refunds if it's ever enabled.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from typing import Any, Callable

from api import gem_webhook

REVENUECAT_API = "https://api.revenuecat.com/v1"


class RevenueCatError(Exception):
    pass


def fetch_subscriber(uid: str, secret_key: str, timeout: float = 10) -> dict[str, Any]:
    """GET /v1/subscribers/{uid} with the secret key. Returns `subscriber`."""
    url = f"{REVENUECAT_API}/subscribers/{urllib.parse.quote(uid, safe='')}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())["subscriber"]
    except urllib.error.HTTPError as e:
        raise RevenueCatError(f"RevenueCat returned {e.code}") from e
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as e:
        raise RevenueCatError(f"RevenueCat request failed: {e}") from e


def _purchased_at_ms(value: str | None) -> int | None:
    if not value:
        return None
    try:
        return int(datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp() * 1000)
    except ValueError:
        return None


def gem_transactions(subscriber: dict[str, Any]) -> list[dict[str, Any]]:
    """Gem-pack transactions as webhook-style events, so the same credit
    logic and Purchases document IDs apply. Store names are upper-cased to
    match webhook events (app_store -> APP_STORE)."""
    events = []
    for product_id, transactions in (subscriber.get("non_subscriptions") or {}).items():
        if not gem_webhook.gems_for_product(product_id):
            continue
        for t in transactions or []:
            tx_id = t.get("store_transaction_id") or t.get("id")
            if not tx_id:
                continue
            events.append({
                "type": "NON_RENEWING_PURCHASE",
                "id": t.get("id"),
                "product_id": product_id,
                "transaction_id": tx_id,
                "store": str(t.get("store") or "store").upper(),
                "environment": "SANDBOX" if t.get("is_sandbox") else "PRODUCTION",
                "purchased_at_ms": _purchased_at_ms(t.get("purchase_date")),
            })
    return events


def sync_user(db, uid: str, fetch: Callable[[str], dict[str, Any]]) -> dict[str, int]:
    """Credits uncredited gem purchases for `uid`. `fetch` returns the
    RevenueCat subscriber object (injected so tests don't call RevenueCat)."""
    subscriber = fetch(uid)
    credited = gems = 0
    for event in gem_transactions(subscriber):
        # Always credit the authenticated user: they asked RevenueCat about
        # their own uid, so these purchases are theirs.
        event["app_user_id"] = uid
        outcome = gem_webhook.handle_event(db, event)
        if outcome.action == "credited":
            credited += 1
            gems += outcome.gems
    return {"credited": credited, "gems": gems}
