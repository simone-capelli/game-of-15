"""Entry point FastAPI.

Avvio:  uvicorn app.main:app --reload --port 8000
Docs:   http://localhost:8000/docs
"""

from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router

app = FastAPI(
    title="Gioco del 15 - API",
    version="0.1.0",
    description="Backend della prova: generatore di partite + classifica in memoria.",
)

# Il frontend Next.js gira su localhost:3000. La regex ammette anche gli
# indirizzi di rete locale (192.168.x.x, 10.x.x.x, 172.16-31.x.x): serve per
# aprire l'app da un altro dispositivo, con uvicorn avviato con --host 0.0.0.0.
# In produzione il dominio del frontend arriva da CORS_ORIGINS (separati da virgola).
_extra_origins = [o.strip() for o in os.environ.get("CORS_ORIGINS", "").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", *_extra_origins],
    allow_origin_regex=r"http://(192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(1[6-9]|2\d|3[01])\.\d+\.\d+):3000",
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
