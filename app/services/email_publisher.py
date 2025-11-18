# app/services/email_publisher.py
import json
from google.cloud.pubsub_v1 import PublisherClient
from app.config import settings


def publish_registration_email(publisher: PublisherClient, *, user_id: str, email: str, full_name: str) -> str:
    """
    Publishes a registration email job to Pub/Sub.
    Returns the published message ID.
    """
    topic_path = publisher.topic_path(settings.gcp_project_id, settings.registration_topic)
    payload = {
        "type": "WELCOME_EMAIL",
        "user_id": user_id,
        "email": email,
        "full_name": full_name,
    }
    future = publisher.publish(topic_path, json.dumps(payload).encode("utf-8"))
    return future.result(timeout=10)
