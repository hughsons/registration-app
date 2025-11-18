# app/config.py
import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from google.cloud import firestore
from google.cloud import pubsub_v1

# Load .env from project root
load_dotenv()

@dataclass(frozen=True)
class Settings:
    gcp_project_id: str = os.getenv("GCP_PROJECT_ID", "demo-registration")

    # Emulators (set as "host:port" when running locally)
    firestore_emulator_host: Optional[str] = os.getenv("FIRESTORE_EMULATOR_HOST")
    pubsub_emulator_host: Optional[str] = os.getenv("PUBSUB_EMULATOR_HOST")

    # Email / SMTP
    smtp_host: str = os.getenv("SMTP_HOST", "localhost")
    smtp_port: int = int(os.getenv("SMTP_PORT", "1025"))
    smtp_user: str = os.getenv("SMTP_USER", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    smtp_use_tls: bool = os.getenv("SMTP_USE_TLS", "false").lower() == "true"
    from_email: str = os.getenv("FROM_EMAIL", "noreply@example.local")

    # Pub/Sub topic and subscription names
    registration_topic: str = os.getenv("REGISTRATION_TOPIC", "registration-emails")
    registration_subscription: str = os.getenv("REGISTRATION_SUBSCRIPTION", "registration-emails-sub")


settings = Settings()


def get_firestore_client() -> firestore.Client:
    """
    Returns a Firestore client. If FIRESTORE_EMULATOR_HOST is set,
    the google-cloud-firestore library auto-routes to the emulator.
    """
    return firestore.Client(project=settings.gcp_project_id)


def get_pubsub_publisher() -> pubsub_v1.PublisherClient:
    """
    Returns a Pub/Sub publisher client.
    PUBSUB_EMULATOR_HOST makes the library use emulator automatically.
    """
    return pubsub_v1.PublisherClient()


def get_pubsub_subscriber() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()
