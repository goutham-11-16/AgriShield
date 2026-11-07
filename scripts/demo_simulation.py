#!/usr/bin/env python3
"""
AgriShield End-to-End Simulation Script
Demonstrates the complete lifecycle: Predict -> Protect -> Recover -> Reconnect
"""
import sys
import os
from datetime import date, timedelta

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.schemas.schemas import (
    CropSuitabilityRequest, DisasterReportCreate, ProduceListingCreate
)
from backend.app.services.crop_service import generate_crop_recommendations
from backend.app.services.weather_service import fetch_weather_and_risks
from backend.app.services.disaster_service import process_disaster_report
from backend.app.services.market_recovery_service import evaluate_and_match_produce
import asyncio

async def run_simulation():
    print("=" * 75)
    print("🌿 AGRISHIELD: COMPLETE AGRICULTURAL LIFECYCLE SIMULATION")
    print("   Target Pilot: Tamil Nadu (Dindigul Horticulture Cluster)")
    print("=" * 75)
    
    # ----------------------------------------------------
    # MODULE A: PREDICT (Before Cultivation)
    # ----------------------------------------------------
    print("\n[MODULE A - PREDICT] Farmer K. Murugan is planning 2.0 acres in Dindigul")
    req = CropSuitabilityRequest(
        district="Dindigul",
        block="Oddanchatram",
        village="Reddiarchatram",
        area_acres=2.0,
        soil_type="Red Sandy Loam",
        soil_ph=6.8,
        irrigation_type="drip",
        water_source="borewell",
        budget_inr=80000.0,
        sowing_date=date.today()
    )
    rec_response = generate_crop_recommendations(req)
    
    print(f"Top Recommended Crops for {req.district}:")
    for idx, c in enumerate(rec_response.recommendations, 1):
        print(f"\n  {idx}. {c.crop_name_ta} ({c.crop_name})")
        print(f"     Suitability: {c.suitability_score}% ({c.suitability_level})")
        print(f"     Expected Harvest Date: {c.expected_harvest_date} ({c.growth_duration_days} days)")
        print(f"     Expected Yield: {c.expected_yield_kg:,.0f} kg • Cultivation Cost: ₹{c.estimated_cultivation_cost_inr:,.0f}")
        print("     Forward Price Scenarios at Harvest Date:")
        print(f"       • Pessimistic (Low Demand):  ₹{c.pessimistic_scenario.price_per_kg}/kg -> Net Profit: ₹{c.pessimistic_scenario.net_profit_inr:,.0f}")
        print(f"       • Normal (Expected):         ₹{c.normal_scenario.price_per_kg}/kg -> Net Profit: ₹{c.normal_scenario.net_profit_inr:,.0f}")
        print(f"       • Optimistic (High Demand):   ₹{c.optimistic_scenario.price_per_kg}/kg -> Net Profit: ₹{c.optimistic_scenario.net_profit_inr:,.0f}")
        
    # ----------------------------------------------------
    # MODULE B: PROTECT (During Cultivation)
    # ----------------------------------------------------
    print("\n" + "-" * 75)
    print("[MODULE B - PROTECT] Day 45 of Tomato Cultivation: Agro-Weather & Early Warnings")
    protect_data = await fetch_weather_and_risks(
        lat=11.1271, lon=78.6569, district_name="Dindigul", crop_name="Tomato", sowing_days_ago=45
    )
    print(f"Current Farm Weather: {protect_data.current_temperature_c}°C, Humidity: {protect_data.current_humidity_pct}%, Rain 24h: {protect_data.precipitation_next_24h_mm}mm")
    print(f"Active Advisories ({len(protect_data.active_alerts)} Alerts):")
    for alert in protect_data.active_alerts:
        print(f"  • [{alert.severity.upper()}] {alert.title_ta} ({alert.title})")
        print(f"    Action: {alert.action_plan_ta}")
        
    # ----------------------------------------------------
    # MODULE C: RECOVER (Post-Disaster Management)
    # ----------------------------------------------------
    print("\n" + "-" * 75)
    print("[MODULE C - RECOVER] Cyclone Inundation Damage: Loss Reporting & PMFBY 72h Rule")
    loss_report = DisasterReportCreate(
        crop_cycle_id="cycle_murugan_01",
        crop_name="Tomato",
        disaster_type="cyclone",
        incident_date=date.today() - timedelta(days=1), # Occurred yesterday
        affected_area_acres=2.0,
        estimated_damage_percentage=70.0,
        notes="Heavy downpour and waterlogging caused standing crop damage."
    )
    recovery_data = process_disaster_report(loss_report)
    print(f"Dossier ID: {recovery_data.report_id}")
    print(f"PMFBY 72h Window Status: {'VALID (On-Time)' if recovery_data.is_within_72h_pmfby else 'EXPIRED'}")
    print(f"Hours Remaining to Intimate Loss: {recovery_data.hours_remaining_for_pmfby} Hours ({recovery_data.urgency_status})")
    print(f"Estimated Tamil Nadu SDRF Input Subsidy: ₹{recovery_data.sdrf_estimated_relief_inr:,.2f}")
    print(f"National Helpline: {recovery_data.pmfby_helpline}")
    print("Action Checklist for Farmer:")
    for step in recovery_data.official_action_checklist_ta[:3]:
        print(f"  {step}")
        
    # ----------------------------------------------------
    # MODULE D: RECONNECT (Salvage & Alternative Buyers)
    # ----------------------------------------------------
    print("\n" + "-" * 75)
    print("[MODULE D - RECONNECT] Salvaging 3,500 kg of Rain-Blemished Tomatoes for Puree Processing")
    listing = ProduceListingCreate(
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
    salvage_data = evaluate_and_match_produce(listing)
    print(f"Safety Check: {salvage_data.safety_status}")
    print(f"Matching Verified Industrial Buyers: {salvage_data.matching_buyers_count} Buyers")
    for q in salvage_data.quotations:
        print(f"\n  • Buyer: {q.buyer_name} ({q.buyer_category})")
        print(f"    Terms: {q.procurement_terms}")
        print(f"    Offered Price: ₹{q.offered_price_per_kg}/kg | Transport Deduction: ₹{q.transport_deduction_per_kg}/kg")
        print(f"    Net Realization per kg: ₹{q.net_realization_per_kg}/kg")
        print(f"    TOTAL NET RECOVERY FOR FARMER: ₹{q.total_net_payout_inr:,.2f}")
        
    print("\n" + "=" * 75)
    print("✅ SIMULATION COMPLETE: AgriShield protected farmer income and recovered value.")
    print("=" * 75)

if __name__ == "__main__":
    asyncio.run(run_simulation())
