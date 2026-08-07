"""
Service layer encapsulating ML model loading, predictions, and metadata retrieval.
"""

import sys
import os

# Ensure project root is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from ml.data_loader import DataLoader
from ml.predictor import DiseasePredictor
from ml.disease_db import DISEASE_DETAILS, get_disease_info
from backend.app.utils.logger import logger


class PredictionService:
    def __init__(self):
        self.data_loader = DataLoader()
        self.predictors = {}

    def get_predictor(self, model_name: str = "random_forest") -> DiseasePredictor:
        if model_name not in self.predictors:
            logger.info(f"Initializing predictor engine for model: {model_name}")
            self.predictors[model_name] = DiseasePredictor(model_name=model_name)
        return self.predictors[model_name]

    def get_symptoms_list(self):
        metadata = self.data_loader.get_symptom_metadata()
        categories = sorted(list(set(item["category"] for item in metadata)))
        return {
            "total_symptoms": len(metadata),
            "categories": categories,
            "symptoms": metadata
        }

    def predict_disease(self, symptoms: list[str], model_name: str = "random_forest") -> dict:
        logger.info(f"Received prediction request with {len(symptoms)} symptoms using model '{model_name}'")
        predictor = self.get_predictor(model_name)
        return predictor.predict(symptoms)

    def get_disease_catalog(self) -> list[dict]:
        catalog = []
        for disease, info in DISEASE_DETAILS.items():
            catalog.append({
                "disease": disease.strip(),
                "description": info["description"],
                "severity": info["severity"],
                "doctor": info["doctor"],
                "precautions": info["precautions"]
            })
        return catalog


prediction_service = PredictionService()
