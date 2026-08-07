"""
FastAPI Router for Disease Prediction Endpoints.
"""

from fastapi import APIRouter, HTTPException, status
from backend.app.models.schemas import (
    PredictRequest, PredictResponse, SymptomListResponse, DiseaseInfoResponse, HealthCheckResponse
)
from backend.app.services.prediction_service import prediction_service
from backend.app.utils.logger import logger

router = APIRouter(prefix="/api", tags=["Disease Prediction"])


@router.get("/health", response_model=HealthCheckResponse)
def health_check():
    """Health check endpoint to verify backend status."""
    try:
        # Test loading default predictor
        predictor = prediction_service.get_predictor("random_forest")
        model_loaded = predictor.model is not None
    except Exception as e:
        logger.error(f"Health check model load error: {e}")
        model_loaded = False

    return {
        "status": "healthy" if model_loaded else "degraded",
        "app_name": "Disease Prediction System",
        "version": "2.0.0",
        "model_loaded": model_loaded
    }


@router.get("/symptoms", response_model=SymptomListResponse)
def get_symptoms():
    """Fetch complete catalog of 130+ symptoms with category tags and display labels."""
    try:
        return prediction_service.get_symptoms_list()
    except Exception as e:
        logger.error(f"Error fetching symptoms: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load symptom catalog: {str(e)}"
        )


@router.post("/predict", response_model=PredictResponse)
def predict_disease(payload: PredictRequest):
    """
    Perform multi-symptom disease inference.
    Returns primary disease prediction, confidence score %, top-3 ranking, precautions, and specialist doctor.
    """
    if not payload.symptoms:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one symptom must be selected for disease prediction."
        )

    try:
        result = prediction_service.predict_disease(
            symptoms=payload.symptoms,
            model_name=payload.model_name or "random_forest"
        )
        return result
    except ValueError as ve:
        logger.warning(f"Validation error in prediction: {ve}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.error(f"Prediction engine error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while evaluating symptoms: {str(e)}"
        )


@router.get("/diseases")
def get_diseases():
    """Fetch complete list of 41 supported medical diagnoses with full clinical metadata."""
    try:
        return prediction_service.get_disease_catalog()
    except Exception as e:
        logger.error(f"Error fetching disease catalog: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load disease catalog: {str(e)}"
        )

