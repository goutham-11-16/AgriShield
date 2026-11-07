import pytest
from datetime import date, timedelta
from backend.app.schemas.schemas import (
    CropSuitabilityRequest, DisasterReportCreate, ProduceListingCreate
)
from backend.app.services.crop_service import generate_crop_recommendations
from backend.app.services.disaster_service import process_disaster_report
from backend.app.services.market_recovery_service import evaluate_and_match_produce

def test_crop_recommendation_and_scenarios():
    req = CropSuitabilityRequest(
        district="Dindigul",
        area_acres=2.5,
        soil_type="Red Sandy Loam",
        soil_ph=6.8,
        irrigation_type="drip",
        budget_inr=100000.0,
        sowing_date=date.today()
    )
    res = generate_crop_recommendations(req)
    
    assert len(res.recommendations) == 3
    for rec in res.recommendations:
        assert rec.crop_name
        assert rec.crop_name_ta
        assert rec.expected_yield_kg > 0
        assert rec.estimated_cultivation_cost_inr > 0
        
        # Verify 3 Forward Price Scenarios ordering
        assert rec.pessimistic_scenario.price_per_kg < rec.normal_scenario.price_per_kg
        assert rec.normal_scenario.price_per_kg < rec.optimistic_scenario.price_per_kg
        
        # Verify economic identity: Revenue - Cost = Net Profit
        assert abs(
            (rec.normal_scenario.total_revenue_inr - rec.normal_scenario.estimated_expenses_inr)
            - rec.normal_scenario.net_profit_inr
        ) < 0.1

def test_disaster_pmfby_72h_rule():
    # Scenario A: Loss reported 1 day after incident (Within 72 Hours)
    report_recent = DisasterReportCreate(
        crop_cycle_id="cycle_01",
        crop_name="Tomato",
        disaster_type="cyclone",
        incident_date=date.today() - timedelta(days=1),
        affected_area_acres=2.0,
        estimated_damage_percentage=65.0
    )
    res_recent = process_disaster_report(report_recent)
    assert res_recent.is_within_72h_pmfby is True
    assert res_recent.hours_remaining_for_pmfby > 0
    assert "URGENT" in res_recent.urgency_status
    assert res_recent.sdrf_estimated_relief_inr > 0 # Eligible for SDRF relief (>33% damage)
    assert "14447" in res_recent.pmfby_helpline

    # Scenario B: Loss reported 5 days after incident (Past standard 72 Hours)
    report_delayed = DisasterReportCreate(
        crop_cycle_id="cycle_02",
        crop_name="Tomato",
        disaster_type="flood",
        incident_date=date.today() - timedelta(days=5),
        affected_area_acres=1.5,
        estimated_damage_percentage=80.0
    )
    res_delayed = process_disaster_report(report_delayed)
    assert res_delayed.is_within_72h_pmfby is False
    assert res_delayed.hours_remaining_for_pmfby == 0.0
    assert "ESCALATED" in res_delayed.urgency_status

def test_market_recovery_safety_and_net_realization():
    # Scenario A: Rotten produce MUST be rejected for safety
    rotten_listing = ProduceListingCreate(
        crop_name="Tomato",
        crop_name_ta="தக்காளி",
        district="Dindigul",
        quantity_kg=2000.0,
        quality_grade="unsafe_rotten",
        harvest_date=date.today(),
        shelf_life_days=1,
        min_expected_price_per_kg=5.0,
        safety_certified_non_rotten=False
    )
    res_rotten = evaluate_and_match_produce(rotten_listing)
    assert "REJECTED" in res_rotten.safety_status
    assert res_rotten.matching_buyers_count == 0
    assert len(res_rotten.quotations) == 0

    # Scenario B: Grade B produce suitable for puree processing
    usable_listing = ProduceListingCreate(
        crop_name="Tomato",
        crop_name_ta="தக்காளி",
        district="Dindigul",
        quantity_kg=3500.0,
        quality_grade="grade_b_processing",
        harvest_date=date.today(),
        shelf_life_days=4,
        min_expected_price_per_kg=8.0,
        safety_certified_non_rotten=True
    )
    res_usable = evaluate_and_match_produce(usable_listing)
    assert "VERIFIED" in res_usable.safety_status
    assert res_usable.matching_buyers_count > 0
    
    # Verify net realization math
    for q in res_usable.quotations:
        expected_net = round(q.offered_price_per_kg - q.transport_deduction_per_kg, 2)
        assert q.net_realization_per_kg == expected_net
        expected_total = round(usable_listing.quantity_kg * expected_net, 2)
        assert q.total_net_payout_inr == expected_total
