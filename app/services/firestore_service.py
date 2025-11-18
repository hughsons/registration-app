# app/services/firestore_service.py
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Tuple

from google.cloud.firestore_v1 import Client
from app.models import RegistrationRequest


USERS_COLLECTION = "users"


def create_user(db: Client, payload: RegistrationRequest) -> Dict[str, Any]:
    """
    Creates a new user in Firestore.
    Returns dict with {id, email, full_name, created_at}.
    """
    doc_ref = db.collection(USERS_COLLECTION).document()  # auto-id
    data = {
        "email": payload.email.lower(),
        "full_name": payload.full_name,
        # Do NOT store plain passwords in real systems – hash & salt (omitted for this demo).
        "created_at": datetime.now(timezone.utc),
    }
    doc_ref.set(data)
    stored = doc_ref.get().to_dict()
    stored["id"] = doc_ref.id
    return stored


def get_user_by_email(db: Client, email: str) -> Optional[Dict[str, Any]]:
    q = (
        db.collection(USERS_COLLECTION)
        .where("email", "==", email.lower())
        .limit(1)
        .stream()
    )
    for doc in q:
        d = doc.to_dict()
        d["id"] = doc.id
        return d
    return None

def list_users(
    db: Client,
    limit: int = 20,
    page_token: Optional[str] = None
) -> Tuple[List[dict], Optional[str]]:
    """
    Returns (users, next_page_token). Ordered by created_at desc.
    page_token is last document id from previous page.
    """
    col = db.collection(USERS_COLLECTION).order_by("created_at", direction="DESCENDING")
    if page_token:
        # start after the last doc from previous page
        last_doc = db.collection(USERS_COLLECTION).document(page_token).get()
        if last_doc.exists:
            col = col.start_after({"created_at": last_doc.to_dict().get("created_at")})
    docs = list(col.limit(limit).stream())

    users: List[dict] = []
    for d in docs:
        item = d.to_dict()
        item["id"] = d.id
        users.append(item)

    next_token = docs[-1].id if len(docs) == limit else None
    return users, next_token
