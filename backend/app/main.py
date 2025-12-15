import json
from pathlib import Path

from fastapi import FastAPI, Request, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import joblib
from sqlalchemy.orm import Session

from .schemas import DiabetesInput, PredictionResponse, PredictionHistoryItem
from .ml.utils import MODEL_PATH
from .ml.predict import predict_diabetes

from .db import engine, Base, get_db
from .models import PredictionRecord

app = FastAPI(title="Diabetes Prediction API", version="1.0.0")

# Ensure backend/data exists (for SQLite DB file)
Path("data").mkdir(parents=True, exist_ok=True)

# Create DB tables (simple approach; later you can use migrations)
Base.metadata.create_all(bind=engine)

# Templates + Static files (Frontend)
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # in production, restrict this
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = None


@app.on_event("startup")
def load_model():
    global MODEL
    if not MODEL_PATH.exists():
        MODEL = None
        print(f"[WARN] Model not found at {MODEL_PATH}. Train first: python -m app.ml.train")
        return
    MODEL = joblib.load(MODEL_PATH)
    print(f"[OK] Model loaded from {MODEL_PATH}")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": MODEL is not None,
        "model_path": str(MODEL_PATH),
    }


@app.post("/api/predict", response_model=PredictionResponse)
def predict(payload: DiabetesInput, db: Session = Depends(get_db)):
    if MODEL is None:
        return PredictionResponse(
            prediction=0,
            probability=0.0,
            label="Model not loaded. Train first: python -m app.ml.train",
        )

    features = payload.model_dump()
    pred, proba = predict_diabetes(MODEL, features)
    label = "Diabetic (higher risk)" if pred == 1 else "Not diabetic (lower risk)"

    # Save prediction to DB
    rec = PredictionRecord(
        inputs_json=json.dumps(features),
        prediction=pred,
        probability=proba,
        label=label,
    )
    db.add(rec)
    db.commit()

    return PredictionResponse(prediction=pred, probability=proba, label=label)


@app.get("/api/history", response_model=list[PredictionHistoryItem])
def history(
    limit: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(PredictionRecord)
        .order_by(PredictionRecord.id.desc())
        .limit(limit)
        .all()
    )

    return [
        PredictionHistoryItem(
            id=r.id,
            created_at=r.created_at,
            prediction=r.prediction,
            probability=r.probability,
            label=r.label,
            inputs=json.loads(r.inputs_json),
        )
        for r in rows
    ]


@app.delete("/api/history")
def clear_history(db: Session = Depends(get_db)):
    deleted = db.query(PredictionRecord).delete()
    db.commit()
    return {"deleted": deleted}
