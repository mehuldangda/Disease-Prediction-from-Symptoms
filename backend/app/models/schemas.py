"""
Pydantic API Schemas for Disease Prediction API.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class SymptomItem(BaseModel):
    id: int
    key: str
    label: str
    category: str


class SymptomListResponse(BaseModel):
    total_symptoms: int
    categories: List[str]
    symptoms: List[SymptomItem]


class PredictRequest(BaseModel):
    symptoms: List[str] = Field(..., min_items=1, description="List of symptom keys selected by user")
    model_name: Optional[str] = Field(default="random_forest", description="ML model to use for prediction")


class DiseasePredictionItem(BaseModel):
    disease: str
    probability: float
    confidence_score: float
    description: str
    severity: str
    doctor: str
    precautions: List[str]


class PredictResponse(BaseModel):
    primary_prediction: str
    confidence_percentage: float
    confidence_score: float
    severity: str
    recommended_doctor: str
    description: str
    precautions: List[str]
    top_3_predictions: List[DiseasePredictionItem]
    matched_symptoms_count: int
    matched_symptoms: List[str]
    unmatched_symptoms: List[str]
    model_used: str


class DiseaseInfoResponse(BaseModel):
    disease: str
    description: str
    severity: str
    doctor: str
    precautions: List[str]


class HealthCheckResponse(BaseModel):
    status: str
    app_name: str
    version: str
    model_loaded: bool
