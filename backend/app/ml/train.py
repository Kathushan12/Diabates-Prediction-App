import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from .utils import DATA_PATH, ARTIFACTS_DIR, MODEL_PATH

EXPECTED_COLS = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
    "Outcome",
]

FEATURES = EXPECTED_COLS[:-1]
TARGET = "Outcome"


def load_dataset() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATA_PATH}\n"
            f"Put your CSV at backend/data/diabetes.csv"
        )

    # First try: assume it has a header
    df = pd.read_csv(DATA_PATH)

    # Your dataset currently has no header → columns look like ['6','148',...]
    # Detect that and reload correctly
    if set(EXPECTED_COLS).issubset(df.columns) is False:
        df = pd.read_csv(DATA_PATH, header=None)
        if df.shape[1] != 9:
            raise ValueError(
                f"Expected 9 columns, but got {df.shape[1]} columns. "
                f"Check your CSV format."
            )
        df.columns = EXPECTED_COLS

    return df


def main():
    df = load_dataset()

    # Ensure numeric types
    for c in EXPECTED_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    X = df[FEATURES]
    y = df[TARGET].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    preprocessor = ColumnTransformer(
        transformers=[("num", numeric_transformer, FEATURES)],
        remainder="drop",
    )

    clf = Pipeline(steps=[
        ("preprocess", preprocessor),
        ("model", LogisticRegression(max_iter=2000)),
    ])

    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print("\n===== Evaluation =====")
    print(f"Accuracy: {acc:.4f}\n")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, preds))
    print("\nClassification Report:")
    print(classification_report(y_test, preds))

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, MODEL_PATH)

    print("\n===== Saved Artifact =====")
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
