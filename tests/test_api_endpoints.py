import pytest
from httpx import AsyncClient, ASGITransport
from datetime import date
from backend.app.main import app

@pytest.mark.asyncio
async def test_health_and_root():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["platform"] == "AgriShield"

        health = await client.get("/health")
        assert health.status_code == 200
        assert health.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_predict_suitability_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "district": "Dindigul",
            "area_acres": 2.0,
            "soil_type": "Red Sandy Loam",
            "irrigation_type": "drip",
            "budget_inr": 90000.0,
            "sowing_date": str(date.today())
        }
        resp = await client.post("/api/v1/predict/suitability", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["recommendations"]) == 3
        assert "தக்காளி" in data["recommendations"][0]["crop_name_ta"] or "நிலக்கடலை" in data["recommendations"][0]["crop_name_ta"]

@pytest.mark.asyncio
async def test_protect_dashboard_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/protect/dashboard?district=Dindigul&crop_name=Tomato&sowing_days_ago=40")
        assert resp.status_code == 200
        data = resp.json()
        assert "Dindigul" in data["location"]
        assert len(data["stage_advisories"]) > 0

@pytest.mark.asyncio
async def test_recover_and_pmfby_endpoints():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. PMFBY Guidelines
        guidelines = await client.get("/api/v1/recover/pmfby-guidelines")
        assert guidelines.status_code == 200
        assert "14447" in guidelines.json()["toll_free_helpline"]
        assert "72 Hours" in guidelines.json()["localized_calamity_rule"]["time_limit"]

        # 2. Report Loss
        payload = {
            "crop_cycle_id": "test_cycle",
            "crop_name": "Tomato",
            "disaster_type": "cyclone",
            "incident_date": str(date.today()),
            "affected_area_acres": 2.0,
            "estimated_damage_percentage": 75.0
        }
        report = await client.post("/api/v1/recover/report-loss", json=payload)
        assert report.status_code == 200
        rep_data = report.json()
        assert rep_data["is_within_72h_pmfby"] is True
        assert rep_data["hours_remaining_for_pmfby"] > 0

@pytest.mark.asyncio
async def test_reconnect_market_endpoints():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Verified buyers
        buyers = await client.get("/api/v1/reconnect/verified-buyers")
        assert buyers.status_code == 200
        assert buyers.json()["count"] > 0

        # List distressed produce
        payload = {
            "crop_name": "Tomato",
            "crop_name_ta": "தக்காளி",
            "district": "Dindigul",
            "quantity_kg": 4000.0,
            "quality_grade": "grade_b_processing",
            "harvest_date": str(date.today()),
            "shelf_life_days": 4,
            "min_expected_price_per_kg": 9.0,
            "safety_certified_non_rotten": True
        }
        listing = await client.post("/api/v1/reconnect/list-produce", json=payload)
        assert listing.status_code == 200
        data = listing.json()
        assert data["matching_buyers_count"] > 0
        assert len(data["quotations"]) > 0

@pytest.mark.asyncio
async def test_offline_sync_push_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "device_id": "android_test_device_001",
            "mutations": [
                {
                    "client_mutation_id": "mut_12345",
                    "entity_type": "DISASTER_REPORT",
                    "operation": "CREATE",
                    "payload": {"loss_pct": 50},
                    "client_timestamp": "2026-11-07T12:00:00"
                }
            ]
        }
        resp = await client.post("/api/v1/sync/push", json=payload)
        assert resp.status_code == 200
        assert resp.json()["processed_count"] == 1
        assert "mut_12345" in resp.json()["acknowledged_mutation_ids"]
