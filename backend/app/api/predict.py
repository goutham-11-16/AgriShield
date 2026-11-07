from fastapi import APIRouter, Query
from typing import Optional
from backend.app.schemas.schemas import CropSuitabilityRequest, CropComparisonResponse
from backend.app.services.crop_service import generate_crop_recommendations, CROPS_DATABASE

router = APIRouter(prefix="/predict", tags=["Module A - Predict"])

@router.post("/suitability", response_model=CropComparisonResponse)
async def evaluate_crops(request: CropSuitabilityRequest):
    """
    Evaluate crop suitability, expected harvest dates, forward seasonal harvest prices,
    and 3-crop side-by-side comparison for the given farm parameters.
    """
    return generate_crop_recommendations(request)

@router.get("/crops")
async def list_available_crops():
    """
    List master agricultural catalog for Tamil Nadu with agronomic duration,
    water requirements, and risk factors.
    """
    return {
        "count": len(CROPS_DATABASE),
        "crops": CROPS_DATABASE
    }
