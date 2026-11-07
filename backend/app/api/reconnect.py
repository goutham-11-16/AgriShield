from fastapi import APIRouter
from backend.app.schemas.schemas import ProduceListingCreate, ProduceListingResponse
from backend.app.services.market_recovery_service import evaluate_and_match_produce, VERIFIED_BUYERS

router = APIRouter(prefix="/reconnect", tags=["Module D - Reconnect"])

@router.post("/list-produce", response_model=ProduceListingResponse)
async def list_distressed_produce(listing: ProduceListingCreate):
    """
    List salvageable/distressed agricultural produce, enforce food safety checks,
    discover verified industrial buyers, and calculate net realization payout.
    """
    return evaluate_and_match_produce(listing)

@router.get("/verified-buyers")
async def list_verified_industrial_buyers():
    """
    List verified food processing factories, puree manufacturers, and livestock feed compounders
    in the Tamil Nadu pilot region.
    """
    return {
        "count": len(VERIFIED_BUYERS),
        "buyers": VERIFIED_BUYERS
    }
