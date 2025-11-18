# Registration App (FastAPI + Firestore + Pub/Sub)

## Prerequisites
- Python 3.12+
- Java 21+ (for Firestore emulator)
- Google Cloud SDK (`gcloud`)
- (Optional) MailHog for viewing emails locally

## 1) Install deps
```
source venv/bin/activate
pip install -U pip setuptools wheel
pip install -r requirements.txt
```
## 2) Create .env
```
GCP_PROJECT_ID=demo-registration
FIRESTORE_EMULATOR_HOST=localhost:8080
PUBSUB_EMULATOR_HOST=localhost:8085

SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_USER=
SMTP_PASSWORD=
SMTP_USE_TLS=false
FROM_EMAIL=noreply@example.local

REGISTRATION_TOPIC=registration-emails
REGISTRATION_SUBSCRIPTION=registration-emails-sub
```

## 3) Start emulators (two terminals)

### Terminal A (Firestore):
```
gcloud beta emulators firestore start --host-port=localhost:8080
```
### Terminal B (Pub/Sub):
```
gcloud beta emulators pubsub start --host-port=localhost:8085
```

## 4) Initialize Pub/Sub (new terminal)
```
source venv/bin/activate
python scripts/init_pubsub.py
```

## 5) Run the API (new terminal)
```
source venv/bin/activate
uvicorn app.main:app --reload
```
## 6) Run the worker (new terminal)
```
source venv/bin/activate
python -m app.workers.email_worker
```

## 7) Testing

## Screenshots 
```
screenshot folder
```

### Form:
 open http://127.0.0.1:8000 and submit.

###  List users:

open http://127.0.0.1:8000/api/users

