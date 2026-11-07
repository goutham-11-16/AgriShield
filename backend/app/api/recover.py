from fastapi import APIRouter
from backend.app.schemas.schemas import DisasterReportCreate, DisasterReportResponse
from backend.app.services.disaster_service import process_disaster_report

router = APIRouter(prefix="/recover", tags=["Module C - Recover"])

@router.post("/report-loss", response_model=DisasterReportResponse)
async def submit_disaster_report(report: DisasterReportCreate):
    """
    Submit crop damage assessment, calculate time elapsed against PMFBY 72h rule,
    determine SDRF relief estimate, and generate official claim dossier.
    """
    return process_disaster_report(report)

@router.get("/pmfby-guidelines")
async def get_pmfby_guidelines():
    """
    Official PMFBY localized calamity guidelines, required evidence, and contact helplines.
    """
    return {
        "scheme_name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "official_portal": "https://pmfby.gov.in/",
        "toll_free_helpline": "14447 / 1800-180-1551",
        "localized_calamity_rule": {
            "time_limit": "72 Hours from occurrence of calamity",
            "eligible_calamities": ["Hailstorm", "Landslide", "Inundation", "Cloudburst", "Natural Fire", "Cyclone"],
            "notified_stages": ["Standing crop (sowing to harvesting)", "Post-harvest losses up to 14 days in field for drying"]
        },
        "required_documents": [
            "Aadhaar Card",
            "Bank Passbook (matching Aadhaar name)",
            "Land Possession Certificate / Patta / Chitta",
            "Crop Sowing Certificate / Adangal issued by VAO",
            "Timestamped geotagged photos of damaged field"
        ],
        "state_relief_provisions": {
            "sdrf_authority": "Tamil Nadu State Disaster Management Authority / CRA",
            "irrigated_crop_norm": "₹17,000 per hectare for crop loss exceeding 33%",
            "rainfed_crop_norm": "₹8,500 per hectare for crop loss exceeding 33%"
        }
    }
