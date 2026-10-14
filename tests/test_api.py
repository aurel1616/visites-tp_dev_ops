import pytest
from fastapi.testclient import TestClient

from app.main import app, redis_client

client = TestClient(app)


@pytest.fixture(autouse=True)
def vider_redis() -> None:
    redis_client.flushdb()


def test_accueil_incremente_le_compteur() -> None:
    premiere_reponse = client.get("/")
    deuxieme_reponse = client.get("/")

    assert premiere_reponse.status_code == 200
    assert premiere_reponse.json() == {"visites": 1}
    assert deuxieme_reponse.json() == {"visites": 2}


def test_health_verifie_redis() -> None:
    reponse = client.get("/health")

    assert reponse.status_code == 200
    assert reponse.json() == {"status": "ok"}


def test_metrics_expose_le_compteur() -> None:
    client.get("/")
    reponse = client.get("/metrics")

    assert reponse.status_code == 200
    assert "visites_total" in reponse.text
