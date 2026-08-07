"""
Evaluation module for assessing trained models and generating comprehensive evaluation reports.
"""

import os
import json
import joblib
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from ml.data_loader import DataLoader


def evaluate_all_models():
    loader = DataLoader()
    X_test, y_test, _, _ = loader.load_test_data()
    save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "saved_model")

    models = ["random_forest", "decision_tree", "mnb", "gradient_boost"]
    summary = {}

    print("==================================================")
    print("Evaluating Saved Models on Test Dataset")
    print("==================================================")

    for m_name in models:
        path = os.path.join(save_dir, f"{m_name}.joblib")
        if not os.path.exists(path):
            print(f"Skipping {m_name} (binary not found)")
            continue

        clf = joblib.load(path)
        preds = clf.predict(X_test)
        acc = accuracy_score(y_test, preds)

        summary[m_name] = {
            "test_accuracy": round(acc * 100, 2),
            "report": classification_report(y_test, preds, output_dict=True)
        }

        print(f"\n--- Model: {m_name} ---")
        print(f"Test Accuracy: {acc * 100:.2f}%")

    eval_file = os.path.join(save_dir, "evaluation_report.json")
    with open(eval_file, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nEvaluation summary written to: {eval_file}")
    return summary


if __name__ == "__main__":
    evaluate_all_models()
