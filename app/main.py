from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pathlib import Path
from datetime import datetime
import os
import json

app = FastAPI(title="api-devops", version="0.1.0")

# Carpeta pensada para montarse como volumen (Docker): -v ./data:/data
DATA_DIR = Path(os.getenv("NOTES_DIR", "/data"))
NOTES_FILE = DATA_DIR / "notes.jsonl"  # JSON Lines: 1 nota por línea (append-only)


def ensure_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not NOTES_FILE.exists():
        NOTES_FILE.touch()


@app.on_event("startup")
def _startup() -> None:
    ensure_storage()


@app.get("/")
def root():
    return {"status": "Running", "message": "API Ready"}


@app.post("/add/{note}")
def add_note(note: str):
    note = note.strip()
    if not note:
        raise HTTPException(status_code=400, detail="La nota no puede estar vacía.")

    ensure_storage()

    record = {
        "note": note,
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }

    # Append seguro y simple
    with NOTES_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return {"status": "added", "record": record}


@app.get("/list")
def list_notes():
    ensure_storage()

    notes = []
    with NOTES_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                notes.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return {"count": len(notes), "notes": notes}
