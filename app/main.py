import os

from fastapi import FastAPI, HTTPException
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from redis import Redis
from redis.exceptions import RedisError
from starlette.responses import Response

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = Redis.from_url(redis_url, decode_responses=True)

visites_total = Counter(
    "visites_total",
    "Nombre total d'appels à la page d'accueil",
)

app = FastAPI(title="API Visites", version="0.1.0")


@app.get("/")
def accueil() -> dict[str, int]:
    nombre = redis_client.incr("visites")
    visites_total.inc()
    return {"visites": nombre}


@app.get("/health")
def health() -> dict[str, str]:
    try:
        redis_client.ping()
    except RedisError as erreur:
        raise HTTPException(
            status_code=503,
            detail="Redis est indisponible",
        ) from erreur

    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> Response:
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
