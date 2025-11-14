# tests/conftest.py
import pytest
from httpx import AsyncClient
from app.main import app
from uuid import uuid4

# --- Fake/Mínimo motor-like DB (simples, em memória) ---
class FakeInsertOneResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id

class FakeCollection:
    def __init__(self, storage):
        self.storage = storage  # list of dicts

    async def find_one(self, query):
        for doc in self.storage:
            matched = True
            for k, v in query.items():
                if doc.get(k) != v:
                    matched = False
                    break
            if matched:
                return doc
        return None

    async def insert_one(self, doc):
        doc_copy = dict(doc)
        doc_copy["_id"] = str(uuid4())
        self.storage.append(doc_copy)
        return FakeInsertOneResult(doc_copy["_id"])

    def find(self, *args, **kwargs):
        class Finder:
            def __init__(self, docs):
                self._docs = docs

            async def to_list(self, length=None):
                return [{k: v for k, v in d.items() if k != "_id"} for d in self._docs]
        return Finder(self.storage)

class FakeDB:
    def __init__(self):
        self._collections = {}

    def get_collection(self, name):
        if name not in self._collections:
            self._collections[name] = []
        return FakeCollection(self._collections[name])

# --- Fixtures ---
@pytest.fixture
async def async_client():
    """
    Fixture que cria um AsyncClient compatível com diferentes versões do httpx.
    Tenta usar `AsyncClient(app=app, ...)` primeiro; se não for aceito, usa ASGITransport.
    """
    client = None
    # tentativa 1: httpx suporta app=app
    try:
        async with AsyncClient(app=app, base_url="http://testserver") as c:
            yield c
            return
    except TypeError:
        # não suportou app=..., tentamos criar via transport ASGI (import interno)
        pass

    # tentativa 2: criar ASGITransport (pode depender da versão do httpx)
    try:
        from httpx._transports.asgi import ASGITransport  # pode ser "privado", mas funciona em muitas versões
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as c:
            yield c
            return
    except Exception:
        # falha ao criar transport; solicitar atualização do httpx
        raise RuntimeError(
            "AsyncClient com app não suportado pela sua versão do httpx. "
            "Execute 'pip install -U httpx' no seu venv ou instale uma versão compatível."
        )

@pytest.fixture
def fake_db(monkeypatch):
    """
    Substitui `app.core.db.db` por um FakeDB em memória.
    """
    from app.core import db as db_core
    fake = FakeDB()
    monkeypatch.setattr(db_core, "db", fake, raising=False)
    return fake
