# API de comptage des visites

Petite API FastAPI qui compte les appels à la page d’accueil. Le compteur est stocké dans Redis et les métriques sont exposées au format Prometheus.

## Prérequis

- Python 3.13 ou plus récent
- Docker

## Installation

Depuis la racine du dépôt :

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"

## Démarrer Redis

Si le conteneur redis n’existe pas encore :

    sudo docker run -d --name redis -p 6379:6379 redis:8-alpine

S’il existe déjà mais est arrêté :

    sudo docker start redis

L’application utilise par défaut redis://localhost:6379/0. Pour modifier cette adresse, définissez la variable REDIS_URL.

## Lancer l’API

Depuis la racine du dépôt et avec l’environnement virtuel activé :

    python -m uvicorn app.main:app --reload

L’API est disponible sur http://127.0.0.1:8000. La documentation interactive FastAPI est disponible sur http://127.0.0.1:8000/docs.

## Routes

- GET / : incrémente et renvoie le compteur de visites.
- GET /health : vérifie la disponibilité de Redis.
- GET /metrics : expose les métriques Prometheus.

## Tests et analyse statique

Depuis la racine du dépôt, avec l’environnement virtuel activé :

    pytest -q
    ruff check .
