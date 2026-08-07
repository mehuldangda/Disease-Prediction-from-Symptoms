"""
Multi-Model Training Module for Disease Prediction.
Trains Decision Tree, Random Forest, Multinomial Naive Bayes, and Gradient Boosting.
Saves model binaries and metadata artifacts to saved_model directory.
"""

import os
import json
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from ml.data_loader import DataLoader, load_config


class ModelTrainer:
    def __init__(self, config_path=None):
        self.loader = DataLoader(config_path) if config_path else DataLoader()
        self.config = self.loader.config
        self.save_dir = os.path.normpath(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), self.config["model_save_path"])
        )
        os.makedirs(self.save_dir, exist_ok=True)

    def train_all(self):
        X_train, y_train, symptom_cols, _ = self.loader.load_training_data()
        X_test, y_test, _, _ = self.loader.load_test_data()

        val_size = self.config["dataset"]["validation_size"]
        random_state = self.config["random_state"]

        X_tr, X_val, y_tr, y_val = train_test_split(
            X_train, y_train, test_size=val_size, random_state=random_state, stratify=y_train
        )

        models = {
            "random_forest": RandomForestClassifier(
                n_estimators=self.config["model"]["random_forest"]["n_estimators"],
                random_state=random_state
            ),
            "decision_tree": DecisionTreeClassifier(
                criterion=self.config["model"]["decision_tree"]["criterion"],
                random_state=random_state
            ),
            "mnb": MultinomialNB(),
            "gradient_boost": GradientBoostingClassifier(
                n_estimators=self.config["model"]["gradient_boost"]["n_estimators"],
                criterion=self.config["model"]["gradient_boost"]["criterion"],
                random_state=random_state
            )
        }

        results = {}

        print("==================================================")
        print("Starting Multi-Model Training & Evaluation")
        print("==================================================")

        for name, clf in models.items():
            print(f"\nTraining Model: {name}...")
            clf.fit(X_tr, y_tr)

            val_acc = accuracy_score(y_val, clf.predict(X_val))
            test_acc = accuracy_score(y_test, clf.predict(X_test))

            model_file = os.path.join(self.save_dir, f"{name}.joblib")
            joblib.dump(clf, model_file)

            results[name] = {
                "val_accuracy": round(val_acc * 100, 2),
                "test_accuracy": round(test_acc * 100, 2),
                "saved_path": model_file
            }
            print(f" -> Validation Accuracy: {val_acc * 100:.2f}%")
            print(f" -> Test Accuracy:       {test_acc * 100:.2f}%")

        # Save feature list metadata
        metadata = {
            "symptoms": symptom_cols,
            "classes": list(clf.classes_),
            "results": results
        }
        with open(os.path.join(self.save_dir, "model_metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)

        print("\n==================================================")
        print("Model training successfully completed!")
        print(f"Artifacts saved in: {self.save_dir}")
        print("==================================================")
        return results


if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.train_all()
