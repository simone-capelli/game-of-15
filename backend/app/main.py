"""Entry point FastAPI.

Avvio:  uvicorn app.main:app --reload --port 8000
Docs:   http://localhost:8000/docs
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router

app = FastAPI(
    title="Gioco del 15 - API",
    version="0.1.0",
    description="Backend della prova: generatore di partite + classifica in memoria.",
)

# Il frontend Next.js gira su localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
