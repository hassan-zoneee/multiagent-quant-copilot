import psycopg
from fastapi import FastAPI, HTTPException

from copilot import __version__
from copilot.db import get_connection

app = FastAPI(title="Quant Research Copilot", version=__version__)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": __version__}


@app.get("/health/db")
def health_db() -> dict:
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
            row = conn.execute(
                "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
            ).fetchone()
    except psycopg.Error as exc:
        raise HTTPException(status_code=503, detail="database unavailable") from exc
    return {"status": "ok", "database": "up", "pgvector": row[0] if row else None}
