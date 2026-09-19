"""
Data Loader Module for Disease Prediction Dataset.
Handles loading CSVs, cleaning features/labels, and extracting symptom metadata.
"""

import os
import pandas as pd
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")


def load_config(config_path=CONFIG_PATH):
    """Load project config YAML file."""
    if not os.path.exists(config_path):
        # Fallback default config
        return {
            "random_state": 101,
            "verbose": True,
            "dataset": {
                "training_data_path": "./dataset/training_data.csv",
                "test_data_path": "./dataset/test_data.csv",
                "validation_size": 0.33
            },
            "model_save_path": "./saved_model/"
        }
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def format_symptom_name(raw_name: str) -> str:
    """Format raw symptom column string into a clean display title."""
    clean = raw_name.strip().replace("_", " ").replace(".", " ")
    # Clean up double spaces or minor typos
    clean = " ".join(clean.split())
    return clean.title()


class DataLoader:
    def __init__(self, config_path=CONFIG_PATH):
        self.config = load_config(config_path)
        self.base_dir = os.path.dirname(os.path.dirname(__file__))

    def _resolve_path(self, relative_path):
        if os.path.isabs(relative_path):
            return relative_path
        return os.path.normpath(os.path.join(self.base_dir, relative_path))

    def load_training_data(self):
        train_path = self._resolve_path(self.config["dataset"]["training_data_path"])
        df = pd.read_csv(train_path)

        # Remove trailing empty columns if any
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # Symptom columns are all columns except prognosis
        symptom_cols = [c for c in df.columns if c.strip() != 'prognosis']
        X = df[symptom_cols]
        y = df['prognosis'].astype(str).str.strip()

        return X, y, symptom_cols, df

    def load_test_data(self):
        test_path = self._resolve_path(self.config["dataset"]["test_data_path"])
        df = pd.read_csv(test_path)

        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        symptom_cols = [c for c in df.columns if c.strip() != 'prognosis']
        X = df[symptom_cols]
        y = df['prognosis'].astype(str).str.strip()

        return X, y, symptom_cols, df

    def get_symptom_metadata(self):
        _, _, symptom_cols, _ = self.load_training_data()
        metadata = []
        for idx, col in enumerate(symptom_cols):
            clean_key = col.strip()
            display_label = format_symptom_name(clean_key)
            category = self._categorize_symptom(clean_key)
            metadata.append({
                "id": idx,
                "key": clean_key,
                "label": display_label,
                "category": category
            })
        return metadata

    def get_symptoms_list(self):
        metadata = self.get_symptom_metadata()
        categories = sorted(list(set(item["category"] for item in metadata)))
        return {
            "total_symptoms": len(metadata),
            "categories": categories,
            "symptoms": metadata
        }

    def _categorize_symptom(self, symptom: str) -> str:
        s = symptom.lower()
        if any(w in s for w in ['rash', 'skin', 'pimple', 'itching', 'blister', 'dusting', 'blackhead', 'peeling', 'nails']):
            return "Dermatological & Skin"
        elif any(w in s for w in ['sneezing', 'cough', 'throat', 'breath', 'sinus', 'runny', 'phlegm', 'chest', 'sputum', 'congestion']):
            return "Respiratory & ENT"
        elif any(w in s for w in ['stomach', 'vomiting', 'nausea', 'diarrhoea', 'indigestion', 'acidity', 'ulcer', 'belly', 'abdomen', 'constipation', 'bowel', 'stool', 'gases']):
            return "Gastrointestinal"
        elif any(w in s for w in ['joint', 'muscle', 'pain', 'cramps', 'neck', 'knee', 'hip', 'stiff', 'limbs', 'walking']):
            return "Musculoskeletal"
        elif any(w in s for w in ['fever', 'chills', 'fatigue', 'sweating', 'lethargy', 'weight', 'malaise', 'dehydration', 'shivering']):
            return "General & Systemic"
        elif any(w in s for w in ['urine', 'micturition', 'bladder', 'polyuria']):
            return "Urinary & Renal"
        elif any(w in s for w in ['headache', 'dizziness', 'spinning', 'balance', 'sensorium', 'slurred', 'paralysis', 'unsteadiness', 'anxiety', 'depression']):
            return "Neurological & Mental Health"
        else:
            return "Other Symptoms"


if __name__ == "__main__":
    loader = DataLoader()
    X_train, y_train, cols, _ = loader.load_training_data()
    print(f"Loaded {len(X_train)} training rows with {len(cols)} symptom features.")
    print(f"Total Unique Prognoses: {len(y_train.unique())}")
