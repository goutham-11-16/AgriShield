from fastapi import APIRouter, Query
from backend.app.schemas.schemas import ProtectDashboardResponse
from backend.app.services.weather_service import fetch_weather_and_risks

router = APIRouter(prefix="/protect", tags=["Module B - Protect"])

@router.get("/dashboard", response_model=ProtectDashboardResponse)
async def get_protect_dashboard(
    latitude: float = Query(11.1271, description="Farm latitude (Dindigul default)"),
    longitude: float = Query(78.6569, description="Farm longitude"),
    district: str = Query("Dindigul", description="District name"),
    crop_name: str = Query("Tomato", description="Cultivated crop"),
    sowing_days_ago: int = Query(45, description="Days elapsed since sowing")
):
    """
    Fetch real-time agro-weather conditions, heavy rain/cyclone early warnings,
    fungal blight humidity risk, and phenological stage-specific advisories.
    """
    return await fetch_weather_and_risks(
        lat=latitude,
        lon=longitude,
        district_name=district,
        crop_name=crop_name,
        sowing_days_ago=sowing_days_ago
    )
