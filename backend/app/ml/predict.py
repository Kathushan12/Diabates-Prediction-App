import pandas as pd

FEATURES = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
]

def predict_diabetes(model, features: dict):
    """
    Returns: (prediction:int, probability:float)
    probability is P(class=1)
    """

    df = pd.DataFrame([{
        "Pregnancies": features["Pregnancies"],
        "Glucose": features["Glucose"],
        "BloodPressure": features["BloodPressure"],
        "SkinThickness": features["SkinThickness"],
        "Insulin": features["Insulin"],
        "BMI": features["BMI"],
        "DiabetesPedigreeFunction": features["DiabetesPedigreeFunction"],
        "Age": features["Age"],
    }], columns=FEATURES)

    proba = float(model.predict_proba(df)[0][1])
    pred = int(proba >= 0.5)
    return pred, proba