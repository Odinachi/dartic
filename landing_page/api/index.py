"""Dartic API, deployed on Vercel next to the static site in public/.

Routes:
  GET  /api/health              liveness check
  POST /api/gems/sync           app-triggered: credits the caller's new gem
                                purchases from RevenueCat (see gem_sync.py)
  POST /api/revenuecat/webhook  RevenueCat webhook (paid plans only); same
                                crediting, plus refunds (see gem_webhook.py)

Environment variables (set in the Vercel project):
  REVENUECAT_SECRET_KEY      required for /api/gems/sync; RevenueCat secret
                             API key (sk_...), never shipped in the app
  REVENUECAT_WEBHOOK_AUTH    required for the webhook; the Authorization value
                             configured on the RevenueCat webhook
  REVENUECAT_WEBHOOK_SECRET  optional; enables HMAC signature checks
  FIREBASE_SERVICE_ACCOUNT   required in production; service-account JSON
  FIREBASE_PROJECT_ID        optional; defaults to dartcoder-d57cb
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from api import gem_sync, gem_webhook

PUBLIC = Path(__file__).resolve().parent.parent / "public"

app = FastAPI(title="Dartic API", docs_url=None, redoc_url=None, openapi_url=None)


@lru_cache(maxsize=1)
def firestore_client():
    import firebase_admin
    from firebase_admin import credentials, firestore

    project_id = os.environ.get("FIREBASE_PROJECT_ID", "dartcoder-d57cb")
    if not firebase_admin._apps:
        service_account = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
        if service_account:
            cred = credentials.Certificate(json.loads(service_account))
            firebase_admin.initialize_app(cred, {"projectId": project_id})
        elif os.environ.get("FIRESTORE_EMULATOR_HOST"):
            firebase_admin.initialize_app(options={"projectId": project_id})
        else:
            raise RuntimeError("FIREBASE_SERVICE_ACCOUNT is not set")
    return firestore.client()


@app.get("/api/health")
def health():
    return {"ok": True}


def verify_firebase_user(authorization: str | None) -> str:
    """Returns the uid from a `Bearer <Firebase ID token>` header."""
    from firebase_admin import auth

    token = (authorization or "").removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=401, detail="sign in required")
    firestore_client()  # initialises firebase_admin
    try:
        return auth.verify_id_token(token)["uid"]
    except Exception:
        raise HTTPException(status_code=401, detail="invalid token")


def fetch_revenuecat_subscriber(uid: str) -> dict:
    secret = os.environ.get("REVENUECAT_SECRET_KEY", "")
    if not secret:
        raise RuntimeError("REVENUECAT_SECRET_KEY is not set")
    return gem_sync.fetch_subscriber(uid, secret)


@app.post("/api/gems/sync")
def sync_gems(request: Request):
    """Called by the signed-in app after a purchase and when the wallet loads.
    Credits any of the caller's gem purchases that haven't been credited yet."""
    uid = verify_firebase_user(request.headers.get("authorization"))
    try:
        result = gem_sync.sync_user(firestore_client(), uid, fetch_revenuecat_subscriber)
    except gem_sync.RevenueCatError as e:
        print(f"gems sync uid={uid}: {e}")
        raise HTTPException(status_code=502, detail="could not reach the store")
    if result["credited"]:
        print(f"gems sync uid={uid}: credited {result['gems']} gems "
              f"from {result['credited']} purchase(s)")
    return result


@app.post("/api/revenuecat/webhook")
async def revenuecat_webhook(request: Request):
    raw = await request.body()

    expected_auth = os.environ.get("REVENUECAT_WEBHOOK_AUTH", "")
    if not gem_webhook.valid_authorization(request.headers.get("authorization"), expected_auth):
        raise HTTPException(status_code=401, detail="unauthorized")

    secret = os.environ.get("REVENUECAT_WEBHOOK_SECRET")
    if secret and not gem_webhook.valid_signature(
            request.headers.get("x-revenuecat-webhook-signature"), raw, secret):
        raise HTTPException(status_code=401, detail="bad signature")

    try:
        event = json.loads(raw)["event"]
    except (ValueError, KeyError, TypeError):
        raise HTTPException(status_code=400, detail="invalid payload")

    # Any exception here returns 500, so RevenueCat retries (~5 times over
    # ~80 minutes). Processing is idempotent per store transaction.
    outcome = gem_webhook.handle_event(firestore_client(), event)
    print(f"revenuecat {event.get('type')} {event.get('id')}: {outcome.action} "
          f"{outcome.gems} gems uid={outcome.uid} {outcome.detail}".strip())
    return {"result": outcome.action, "gems": outcome.gems}


@app.exception_handler(StarletteHTTPException)
async def not_found(request: Request, exc: StarletteHTTPException):
    """Unknown non-API paths get the site's 404 page instead of JSON."""
    page = PUBLIC / "404.html"
    if exc.status_code == 404 and not request.url.path.startswith("/api/") and page.exists():
        return HTMLResponse(page.read_text(), status_code=404)
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
