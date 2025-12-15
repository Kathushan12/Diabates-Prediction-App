from pathlib import Path

# This file is at: backend/app/ml/utils.py
# parents:
# 0 = ml
# 1 = app
# 2 = backend
BACKEND_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = BACKEND_DIR / "data" / "diabetes.csv"
ARTIFACTS_DIR = BACKEND_DIR / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "model.joblib"
