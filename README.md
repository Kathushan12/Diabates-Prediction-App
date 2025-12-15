# Diabetes Prediction App (ML + FastAPI + Docker + Database)

A full-stack machine learning web application that predicts diabetes risk using common medical features (e.g., glucose, BMI, age).  
Includes model training, a FastAPI backend, a modern animated UI, and database-backed prediction history.

> **Disclaimer:** For educational purposes only — not medical advice.

---

## ✨ Features

- ✅ **Model training + saved artifact** (`artifacts/model.joblib`)
- ✅ **FastAPI REST API**
  - `POST /api/predict` → prediction + probability
  - `GET /api/history` → stored prediction history (DB)
  - `DELETE /api/history` → clear prediction history
  - `GET /health` → API health status
- ✅ **Frontend UI (Jinja2 + HTML/CSS/JS)**
  - Modern animated UI
  - Dark/Light theme toggle
  - Real-time prediction feedback
  - Recent predictions section
- ✅ **Database persistence (SQLAlchemy)**
  - Local default: SQLite
  - PostgreSQL-ready via `DATABASE_URL` env var
- ✅ **Dockerized** for consistent builds and easy deployment

---

## ✅ Requirements

- Python 3.10+ (recommended: 3.11)
- pip
- (Optional) Docker Desktop

---

## ⚙️ Setup (Local - VS Code / Windows)

### 1) Create and activate a virtual environment
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
### 2) Install dependencies
```powershell
pip install -r requirements.txt
```

### 3) Add dataset (Place the CSV at:)
```powershell
backend/data/diabetes.csv
```

### 4) 🧠 Train the Model (This creates: backend/artifacts/model.joblib)
```powershell
cd backend
python -m app.ml.train

```
### ▶️ Run the App Locally
```powershell
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

```


### 🐳 Run with Docker
```powershell
docker build -t diabetes-app .
docker run -p 8001:8000 diabetes-app
```
### Then Open this link :- http://127.0.0.1:8001/


---
### 📌 Disclaimer
This project is for learning/demonstration only and should not be used for real medical decisions.

###  👤 Author
GitHub: https://github.com/Kathushan12

LinkedIn: www.linkedin.com/in/kathushan12
