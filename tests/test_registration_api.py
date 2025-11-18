# tests/test_registration_api.py
import json
from fastapi.testclient import TestClient
from app.main import app
from app.config import get_firestore_client
from unittest.mock import MagicMock

class DummyDB:
    def __init__(self):
        self.users = {}

    def collection(self, name):
        assert name == "users"
        return self

    def document(self):
        from uuid import uuid4
        class Doc:
            def __init__(self, store):
                self._id = uuid4().hex[:12]
                self._store = store
                self._data = None
            def set(self, data):
                self._data = data
                self._store[self._id] = data
            def get(self):
                class G:
                    def __init__(self, d):
                        self._d = d
                    def to_dict(self):
                        return self._d
                return G(self._data)
            @property
            def id(self):
                return self._id
        return Doc(self.users)

    def where(self, field, op, value):
        assert field == "email" and op == "=="
        class Q:
            def __init__(self, users, email):
                self._users = users
                self._email = email
            def limit(self, n):
                return self
            def stream(self):
                for k, v in self._users.items():
                    if v.get("email") == self._email:
                        class Doc:
                            def __init__(self, id, d):
                                self._id = id
                                self._d = d
                            def to_dict(self): return self._d
                            @property
                            def id(self): return self._id
                        yield Doc(k, v)
        return Q(self.users, value)

def test_register_success(monkeypatch):
    # Override Firestore dependency
    dummy_db = DummyDB()
    app.dependency_overrides[get_firestore_client] = lambda: dummy_db

    # Stub Pub/Sub publisher call
    from app.services import email_publisher
    monkeypatch.setattr(email_publisher, "publish_registration_email", lambda *args, **kwargs: "msg-123")

    client = TestClient(app)
    payload = {"email":"a@b.com","full_name":"Alice","password":"secret12"}
    r = client.post("/api/register", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["email"] == "a@b.com"
    assert body["full_name"] == "Alice"
