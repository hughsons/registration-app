# scripts/init_pubsub.py
import os
from google.cloud import pubsub_v1

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "demo-registration")
TOPIC = os.getenv("REGISTRATION_TOPIC", "registration-emails")
SUB = os.getenv("REGISTRATION_SUBSCRIPTION", "registration-emails-sub")

def main():
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    topic_path = publisher.topic_path(PROJECT_ID, TOPIC)
    sub_path = subscriber.subscription_path(PROJECT_ID, SUB)

    # Create topic if not exists
    try:
        publisher.get_topic(request={"topic": topic_path})
        print(f"Topic exists: {topic_path}")
    except Exception:
        publisher.create_topic(request={"name": topic_path})
        print(f"Topic created: {topic_path}")

    # Create subscription if not exists
    try:
        subscriber.get_subscription(request={"subscription": sub_path})
        print(f"Subscription exists: {sub_path}")
    except Exception:
        subscriber.create_subscription(
            request={"name": sub_path, "topic": topic_path}
        )
        print(f"Subscription created: {sub_path}")

if __name__ == "__main__":
    main()
