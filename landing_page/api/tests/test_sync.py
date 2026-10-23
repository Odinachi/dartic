"""Tests for POST /api/gems/sync (Firestore emulator; see test_webhook.py).

The Firebase token check and the RevenueCat call are replaced with fakes;
crediting runs for real against the emulator.
"""

import os
import sys
from pathlib import Path

import pytest
from fastapi import HTTPException

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # landing_page/
os.environ.setdefault("FIREBASE_PROJECT_ID", "demo-dartic")

if not os.environ.get("FIRESTORE_EMULATOR_HOST"):
    pytest.skip("Firestore emulator not running", allow_module_level=True)

from fastapi.testclient import TestClient  # noqa: E402

from api import gem_sync, gem_webhook  # noqa: E402
from api import index as server  # noqa: E402

client = TestClient(server.app)
db = server.firestore_client()
TOKENS = {"Bearer alice-token": "alice", "Bearer bob-token": "bob"}
SUBSCRIBERS: dict[str, dict] = {}


def tx(id_, store_tx=None, date="2026-10-20T10:00:00Z", store="app_store", sandbox=True):
    t = {"id": id_, "purchase_date": date, "store": store, "is_sandbox": sandbox}
    if store_tx:
        t["store_transaction_id"] = store_tx
    return t


@pytest.fixture(autouse=True)
def fakes(monkeypatch):
    def verify(header):
        if header not in TOKENS:
            raise HTTPException(status_code=401, detail="invalid token")
        return TOKENS[header]

    def fetch(uid):
        if uid == "broken":
            raise gem_sync.RevenueCatError("RevenueCat returned 500")
        return SUBSCRIBERS.get(uid, {"non_subscriptions": {}})

    monkeypatch.setattr(server, "verify_firebase_user", verify)
    monkeypatch.setattr(server, "fetch_revenuecat_subscriber", fetch)
    SUBSCRIBERS.clear()
    for collection in ("Purchases", "Users"):
        for doc in db.collection(collection).list_documents():
            for sub in doc.collections():
                for d in sub.list_documents():
                    d.delete()
            doc.delete()
    yield


def sync(token="Bearer alice-token"):
    return client.post("/api/gems/sync", headers={"Authorization": token} if token else {})


def wallet(uid):
    snap = db.document(f"Users/{uid}/wallet/main").get()
    return snap.to_dict() if snap.exists else None


def test_requires_a_valid_firebase_token():
    assert sync(token=None).status_code == 401
    assert sync(token="Bearer forged").status_code == 401


def test_credits_new_gem_purchases():
    SUBSCRIBERS["alice"] = {"non_subscriptions": {
        "dartic_gems_10": [tx("rc1", "1000001")],
        "dartic_gems_30": [tx("rc2", "1000002")],
    }}
    r = sync()
    assert r.status_code == 200 and r.json() == {"credited": 2, "gems": 40}
    assert wallet("alice")["gems"] == gem_webhook.WELCOME_BONUS + 40
    p = db.document("Purchases/APP_STORE_1000001").get().to_dict()
    assert p["uid"] == "alice" and p["gems"] == 10 and p["environment"] == "SANDBOX"


def test_repeat_syncs_never_double_credit():
    SUBSCRIBERS["alice"] = {"non_subscriptions": {"dartic_gems_10": [tx("rc1", "1000001")]}}
    sync()
    assert sync().json() == {"credited": 0, "gems": 0}
    assert wallet("alice")["gems"] == gem_webhook.WELCOME_BONUS + 10


def test_only_new_purchases_are_credited_later():
    SUBSCRIBERS["alice"] = {"non_subscriptions": {"dartic_gems_10": [tx("rc1", "1000001")]}}
    sync()
    SUBSCRIBERS["alice"]["non_subscriptions"]["dartic_gems_10"].append(tx("rc3", "1000003"))
    assert sync().json() == {"credited": 1, "gems": 10}
    assert wallet("alice")["gems"] == gem_webhook.WELCOME_BONUS + 20


def test_same_key_as_webhook_so_paths_never_double_credit():
    # Webhook credited first (store transaction id), then the app syncs.
    db.document("Users/alice/wallet/main").set({"gems": 5, "unlocked": [], "rewarded": []})
    gem_webhook.handle_event(db, {
        "type": "NON_RENEWING_PURCHASE", "id": "evt", "app_user_id": "alice",
        "product_id": "dartic_gems_10", "transaction_id": "1000001", "store": "APP_STORE",
    })
    SUBSCRIBERS["alice"] = {"non_subscriptions": {"dartic_gems_10": [tx("rc1", "1000001")]}}
    assert sync().json()["credited"] == 0
    assert wallet("alice")["gems"] == 15


def test_falls_back_to_revenuecat_id_and_normalises_store():
    SUBSCRIBERS["alice"] = {"non_subscriptions": {
        "dartic_gems_10": [tx("rc9", store="play_store", sandbox=False)]}}
    sync()
    p = db.document("Purchases/PLAY_STORE_rc9").get().to_dict()
    assert p["environment"] == "PRODUCTION" and p["gems"] == 10


def test_ignores_non_gem_products_and_existing_wallet_is_kept():
    db.document("Users/alice/wallet/main").set({"gems": 2, "unlocked": ["p1"], "rewarded": []})
    SUBSCRIBERS["alice"] = {"non_subscriptions": {
        "dartic_pro_lifetime": [tx("rc5", "5")],
        "dartic_gems_10": [tx("rc6", "6")],
    }}
    assert sync().json() == {"credited": 1, "gems": 10}
    w = wallet("alice")
    assert w["gems"] == 12 and w["unlocked"] == ["p1"]


def test_users_only_get_their_own_purchases():
    SUBSCRIBERS["alice"] = {"non_subscriptions": {"dartic_gems_10": [tx("rc1", "1")]}}
    assert sync(token="Bearer bob-token").json() == {"credited": 0, "gems": 0}
    assert wallet("bob") is None


def test_revenuecat_failure_is_502_and_changes_nothing():
    TOKENS["Bearer broken-token"] = "broken"
    r = sync(token="Bearer broken-token")
    assert r.status_code == 502
    assert wallet("broken") is None


def test_purchase_date_parsing():
    assert gem_sync._purchased_at_ms("2026-10-20T10:00:00Z") == 1792490400000
    assert gem_sync._purchased_at_ms(None) is None
    assert gem_sync._purchased_at_ms("garbage") is None
