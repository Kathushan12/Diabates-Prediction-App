from datetime import datetime
from sqlalchemy import Integer, Float, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class PredictionRecord(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    # Store inputs as JSON string for SQLite compatibility
    inputs_json: Mapped[str] = mapped_column(Text, nullable=False)

    prediction: Mapped[int] = mapped_column(Integer, nullable=False)
    probability: Mapped[float] = mapped_column(Float, nullable=False)
    label: Mapped[str] = mapped_column(String(120), nullable=False)
