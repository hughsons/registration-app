# app/main.py
from fastapi import FastAPI, Request, Depends, status, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Query

from app.config import settings, get_firestore_client, get_pubsub_publisher
from app.models import RegistrationRequest, RegistrationResponse
from app.services.firestore_service import create_user, get_user_by_email
from app.services.email_publisher import publish_registration_email
from app.models import UserListResponse, UserItem
from app.services.firestore_service import list_users

from typing import Optional
app = FastAPI(title="Registration App")

# Static + templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/api/register", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    payload: RegistrationRequest,
    db=Depends(get_firestore_client),
):
    # Simple duplicate-check
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered.")

    stored = create_user(db, payload)

    # Publish async email job
    publisher = get_pubsub_publisher()
    publish_registration_email(
        publisher,
        user_id=stored["id"],
        email=stored["email"],
        full_name=stored["full_name"],
    )

    return RegistrationResponse(
        id=stored["id"],
        email=stored["email"],
        full_name=stored["full_name"],
        created_at=stored["created_at"],
    )


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/users", response_model=UserListResponse)
def list_users_api(
    db=Depends(get_firestore_client),
    limit: int = Query(20, ge=1, le=100),
    page_token: Optional[str] = Query(None, description="Use next_page_token from previous response")
):
    """Dev-only: list users from Firestore with simple pagination."""
    items, next_token = list_users(db, limit=limit, page_token=page_token)
    return UserListResponse(
        items=[UserItem(**i) for i in items],
        next_page_token=next_token
    )