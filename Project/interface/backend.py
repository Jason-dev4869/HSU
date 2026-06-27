"""
FastAPI backend for the multilingual NER demo.
Loads the FINAL/OFFICIAL model (produced by train_mner_wikiann.py,
saved at PRODUCTION_DIR) and exposes a single /predict endpoint
consumed by index.html.

Run:
    pip install fastapi uvicorn transformers torch --break-system-packages
    uvicorn backend:app --reload --port 8000
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
from pathlib import Path

# Must match PRODUCTION_DIR in train_mner_wikiann.py
PRODUCTION_DIR = str(Path(__file__).resolve().parent.parent / "mner-production")

app = FastAPI(title="Multilingual NER API")

# Allow the static HTML file (opened from disk or a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp = pipeline(
    "ner",
    model=PRODUCTION_DIR,
    tokenizer=PRODUCTION_DIR,
    aggregation_strategy="simple"
)


class TextIn(BaseModel):
    text: str


@app.post("/predict")
def predict(payload: TextIn):
    raw_entities = nlp(payload.text)
    entities = [
        {
            "text": e["word"],
            "label": e["entity_group"],
            "start": int(e["start"]),
            "end": int(e["end"]),
            "score": round(float(e["score"]), 4),
        }
        for e in raw_entities
    ]
    return {"text": payload.text, "entities": entities}


@app.get("/health")
def health():
    return {"status": "ok", "model_dir": PRODUCTION_DIR}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)