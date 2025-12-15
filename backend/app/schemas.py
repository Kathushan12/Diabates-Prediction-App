from datetime import datetime
from pydantic import BaseModel, Field


class DiabetesInput(BaseModel):
    Pregnancies: float = Field(ge=0)
    Glucose: float = Field(ge=0)
    BloodPressure: float = Field(ge=0)
    SkinThickness: float = Field(ge=0)
    Insulin: float = Field(ge=0)
    BMI: float = Field(ge=0)
    DiabetesPedigreeFunction: float = Field(ge=0)
    Age: float = Field(ge=0)


class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    label: str


class PredictionHistoryItem(BaseModel):
    id: int
    created_at: datetime
    prediction: int
    probability: float
    label: str
    inputs: dict
