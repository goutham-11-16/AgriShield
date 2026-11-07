from fastapi import APIRouter
from backend.app.schemas.schemas import SyncPushRequest, SyncPushResponse
from backend.app.services.sync_service import process_offline_sync

router = APIRouter(prefix="/sync", tags=["Offline-First Synchronization"])

@router.post("/push", response_model=SyncPushResponse)
async def sync_offline_mutations(batch: SyncPushRequest):
    """
    Ingest queued mutations from offline Android clients idempotently and return acknowledgments.
    """
    return await process_offline_sync(batch)
