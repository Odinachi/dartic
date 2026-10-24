"""Webhook tests. They need the Firestore emulator:

    cd landing_page
    pip install "fastapi>=0.118,<1" "firebase-admin>=6.9,<8" httpx pytest
    firebase emulators:exec --only firestore --project demo-dartic \
        "FIREBASE_PROJECT_ID=demo-dartic python -m pytest -q"
"""

import hashlib
import hmac
import json
import os
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # landing_page/

os.environ.setdefault("FIREBASE_PROJECT_ID", "demo-dartic")
os.environ["REVENUECAT_WEBHOOK_AUTH"] = "Bearer test-auth"
os.environ.pop("REVENUECAT_WEBHOOK_SECRET", None)

if not os.environ.get("FIRESTORE_EMULATOR_HOST"):
    pytest.skip("Firestore emulator not running", allow_module_level=True)

from fastapi.testclient import TestClient  # noqa: E402

from api import gem_webhook  # noqa: E402
from api import index as server  # noqa: E402

client = TestClient(server.app)
db = server.firestore_client()
AUTH = {"Authorization": "Bearer test-auth"}


def wallet(uid):
    snap = db.document(f"Users/{uid}/wallet/main").get()
    return snap.to_dict() if snap.exists else None


def purchase_event(**overrides):
    event = {
        "id": "evt-1",
        "type": "NON_RENEWING_PURCHASE",
        "app_user_id": "alice",
        "original_app_user_id": "$RCAnonymousID:abc",
        "aliases": ["$RCAnonymousID:abc", "alice"],
        "product_id": "dartic_gems_10",
        "transaction_id": "tx-1",
        "store": "APP_STORE",
        "environment": "SANDBOX",
        "purchased_at_ms": 1_760_000_000_000,
    }
    event.update(overrides)
    return {"api_version": "1.0", "event": event}


def post(body, headers=AUTH):
    return client.post("/api/revenuecat/webhook", content=json.dumps(body), headers=headers)


@pytest.fixture(autouse=True)
def clean():
    for collection in ("Purchases", "Users"):
        for doc in db.collection(collection).list_documents():
            for sub in doc.collections():
                for d in sub.list_documents():
                    d.delete()
            doc.delete()
    yield


# ── pure helpers ──────────────────────────────────────────────

def test_gems_for_product():
    assert gem_webhook.gems_for_product("dartic_gems_10") == 10
    assert gem_webhook.gems_for_product("dartic_gem_30") == 30
    assert gem_webhook.gems_for_product("dartic_gem_100") == 100
    assert gem_webhook.gems_for_product("dartic_gems_25:base") == 25
    assert gem_webhook.gems_for_product("dartic_pro") is None
    assert gem_webhook.gems_for_product(None) is None


def test_firebase_uid_skips_anonymous_ids():
    assert gem_webhook.firebase_uid({"app_user_id": "$RCAnonymousID:x", "aliases": ["$RCAnonymousID:x", "bob"]}) == "bob"
    assert gem_webhook.firebase_uid({"app_user_id": "$RCAnonymousID:x"}) is None


def test_signature_check():
    raw, secret, t = b'{"event":{}}', "s3cret", int(time.time())
    sig = hmac.new(secret.encode(), f"{t}.".encode() + raw, hashlib.sha256).hexdigest()
    assert gem_webhook.valid_signature(f"t={t},v1={sig}", raw, secret)
    assert not gem_webhook.valid_signature(f"t={t},v1={sig}", raw + b" ", secret)
    assert not gem_webhook.valid_signature(f"t={t - 3600},v1={sig}", raw, secret)
    assert not gem_webhook.valid_signature("garbage", raw, secret)


# ── webhook endpoint ──────────────────────────────────────────

def test_rejects_missing_or_wrong_authorization():
    assert post(purchase_event(), headers={}).status_code == 401
    assert post(purchase_event(), headers={"Authorization": "Bearer nope"}).status_code == 401
    assert wallet("alice") is None


def test_purchase_creates_wallet_with_bonus_plus_gems():
    r = post(purchase_event())
    assert r.status_code == 200 and r.json() == {"result": "credited", "gems": 10}
    w = wallet("alice")
    assert w["gems"] == gem_webhook.WELCOME_BONUS + 10
    assert w["unlocked"] == [] and w["rewarded"] == []
    p = db.document("Purchases/APP_STORE_tx-1").get().to_dict()
    assert p["uid"] == "alice" and p["gems"] == 10 and p["status"] == "credited"


def test_purchase_adds_to_existing_wallet():
    db.document("Users/alice/wallet/main").set({"gems": 1, "unlocked": ["p1"], "rewarded": []})
    post(purchase_event())
    w = wallet("alice")
    assert w["gems"] == 11 and w["unlocked"] == ["p1"]


def test_retried_webhook_credits_once():
    post(purchase_event())
    r = post(purchase_event())
    assert r.json()["result"] == "duplicate"
    assert wallet("alice")["gems"] == gem_webhook.WELCOME_BONUS + 10


def test_two_purchases_both_credit():
    post(purchase_event())
    post(purchase_event(id="evt-2", transaction_id="tx-2", product_id="dartic_gems_30"))
    assert wallet("alice")["gems"] == gem_webhook.WELCOME_BONUS + 40


def test_ignores_non_gem_products_and_other_events():
    assert post(purchase_event(product_id="dartic_pro")).json()["result"] == "ignored"
    assert post(purchase_event(type="INITIAL_PURCHASE")).json()["result"] == "ignored"
    assert post(purchase_event(type="TEST")).json()["result"] == "ignored"
    assert wallet("alice") is None


def test_ignores_anonymous_purchases():
    body = purchase_event(app_user_id="$RCAnonymousID:x", original_app_user_id="$RCAnonymousID:x", aliases=[])
    assert post(body).json()["result"] == "ignored"


def test_refund_takes_gems_back():
    post(purchase_event())
    r = post(purchase_event(id="evt-r", type="CANCELLATION", cancel_reason="CUSTOMER_SUPPORT"))
    assert r.json() == {"result": "refunded", "gems": 10}
    assert wallet("alice")["gems"] == gem_webhook.WELCOME_BONUS
    assert db.document("Purchases/APP_STORE_tx-1").get().get("status") == "refunded"
    # A repeated refund does nothing.
    assert post(purchase_event(id="evt-r2", type="CANCELLATION")).json()["result"] == "ignored"
    assert wallet("alice")["gems"] == gem_webhook.WELCOME_BONUS


def test_refund_never_goes_below_zero():
    post(purchase_event())
    db.document("Users/alice/wallet/main").update({"gems": 4})  # spent most gems
    r = post(purchase_event(id="evt-r", type="CANCELLATION"))
    assert r.json() == {"result": "refunded", "gems": 4}
    assert wallet("alice")["gems"] == 0


def test_refund_without_purchase_is_ignored():
    assert post(purchase_event(type="CANCELLATION")).json()["result"] == "ignored"


def test_bad_payload_is_400():
    r = client.post("/api/revenuecat/webhook", content=b"not json", headers=AUTH)
    assert r.status_code == 400


def test_health_and_html_404():
    assert client.get("/api/health").json() == {"ok": True}
    r = client.get("/no-such-page")
    assert r.status_code == 404 and "Page not found" in r.text
    assert client.get("/api/nope").json() == {"detail": "Not Found"}
