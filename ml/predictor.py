"""
Inference Engine Module for Disease Prediction.
Loads trained classifier, processes input symptoms, calculates confidence scores,
ranks top 3 predictions, and enriches response with medical metadata.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from ml.disease_db import get_disease_info


class DiseasePredictor:
    def __init__(self, model_name="random_forest"):
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.save_dir = os.path.join(self.base_dir, "saved_model")
        self.model_name = model_name
        self.model = None
        self.symptoms_list = []
        self.classes = []
        self._load_resources()

    def _load_resources(self):
        model_path = os.path.join(self.save_dir, f"{self.model_name}.joblib")
        metadata_path = os.path.join(self.save_dir, "model_metadata.json")

        if not os.path.exists(model_path) or not os.path.exists(metadata_path):
            # Auto-trigger training if model files don't exist
            print("Model binaries not found. Triggering auto-training...")
            from ml.train import ModelTrainer
            trainer = ModelTrainer()
            trainer.train_all()

        self.model = joblib.load(model_path)

        with open(metadata_path, "r") as f:
            meta = json.load(f)
            self.symptoms_list = meta["symptoms"]
            self.classes = list(self.model.classes_)

    def predict(self, input_symptoms: list) -> dict:
        """
        Given a list of symptom string keys, construct feature vector and predict top-3 disease diagnoses.
        """
        if not input_symptoms:
            raise ValueError("At least one symptom must be selected for disease prediction.")

        # Create binary feature vector
        vector = [0] * len(self.symptoms_list)
        matched_symptoms = []
        unmatched_symptoms = []

        # Map input symptoms (case-insensitive & whitespace trimmed)
        normalized_symptoms = [s.strip().lower() for s in input_symptoms]

        for idx, symptom in enumerate(self.symptoms_list):
            norm_key = symptom.strip().lower()
            if norm_key in normalized_symptoms:
                vector[idx] = 1
                matched_symptoms.append(symptom)

        for user_sym in input_symptoms:
            if user_sym.strip().lower() not in [s.strip().lower() for s in self.symptoms_list]:
                unmatched_symptoms.append(user_sym)

        if sum(vector) == 0:
            raise ValueError(f"None of the provided symptoms ({', '.join(input_symptoms)}) were recognized by the model.")

        df_input = pd.DataFrame([vector], columns=self.symptoms_list)

        # Get probabilities across all classes
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(df_input)[0]
        else:
            # Fallback for models without predict_proba
            pred_class = self.model.predict(df_input)[0]
            probs = [1.0 if c == pred_class else 0.0 for c in self.classes]

        # Rank diseases by probability
        ranked_indices = np.argsort(probs)[::-1]

        top_predictions = []
        for rank_idx in ranked_indices[:3]:
            disease = str(self.classes[rank_idx]).strip()
            prob = float(probs[rank_idx])
            info = get_disease_info(disease)
            top_predictions.append({
                "disease": disease,
                "probability": round(prob * 100, 2),
                "confidence_score": round(prob, 4),
                "description": info["description"],
                "severity": info["severity"],
                "doctor": info["doctor"],
                "precautions": info["precautions"]
            })

        primary = top_predictions[0]

        return {
            "primary_prediction": primary["disease"],
            "confidence_percentage": primary["probability"],
            "confidence_score": primary["confidence_score"],
            "severity": primary["severity"],
            "recommended_doctor": primary["doctor"],
            "description": primary["description"],
            "precautions": primary["precautions"],
            "top_3_predictions": top_predictions,
            "matched_symptoms_count": sum(vector),
            "matched_symptoms": matched_symptoms,
            "unmatched_symptoms": unmatched_symptoms,
            "model_used": self.model_name
        }


if __name__ == "__main__":
    predictor = DiseasePredictor()
    sample_symptoms = ["itching", "skin_rash", "nodal_skin_eruptions"]
    result = predictor.predict(sample_symptoms)
    print("Prediction Result:")
    print(json.dumps(result, indent=2))
