# app/workers/email_worker.py
import json
import threading
from concurrent.futures import TimeoutError
from google.cloud.pubsub_v1 import SubscriberClient
from app.config import settings, get_pubsub_subscriber
from app.services.email_sender import send_welcome_email


def _callback(message):
    try:
        data = json.loads(message.data.decode("utf-8"))
        if data.get("type") == "WELCOME_EMAIL":
            send_welcome_email(data["email"], data.get("full_name", "there"))
        message.ack()
    except Exception as exc:
        # In production: consider NACK with dead-letter queues & retry policies.
        print(f"Worker error: {exc}")
        message.nack()


def run_worker(blocking: bool = True):
    subscriber: SubscriberClient = get_pubsub_subscriber()
    subscription_path = subscriber.subscription_path(
        settings.gcp_project_id, settings.registration_subscription
    )

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=_callback)
    print(f"Worker listening on {subscription_path}...")

    if blocking:
        try:
            streaming_pull_future.result()
        except KeyboardInterrupt:
            streaming_pull_future.cancel()
            streaming_pull_future.result()
    else:
        # Non-blocking start (useful for tests)
        threading.Thread(target=lambda: streaming_pull_future.result(), daemon=True).start()


if __name__ == "__main__":
    run_worker(blocking=True)
