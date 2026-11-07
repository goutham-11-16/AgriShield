from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import date, datetime

# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    preferred_language: str
    user_id: str

class UserCreate(BaseModel):
    phone_number: str
    full_name: str
    password: str
    role: str = "farmer"
    preferred_language: str = "ta"
    district: str = "Dindigul"
    block: str = "Oddanchatram"
    village: str = "Reddiarchatram"

# --- Module A: Predict Schemas ---
class CropSuitabilityRequest(BaseModel):
    district: str = "Dindigul"
    block: Optional[str] = "Oddanchatram"
    village: Optional[str] = "Reddiarchatram"
    area_acres: float = Field(default=2.0, gt=0)
    soil_type: str = "Red Sandy Loam"
    soil_ph: Optional[float] = 6.8
    irrigation_type: str = "drip" # drip, sprinkler, flood, rainfed
    water_source: str = "borewell" # borewell, open_well, canal, tank, none
    budget_inr: float = Field(default=80000.0, gt=0)
    sowing_date: Optional[date] = None
    preferred_crops: Optional[List[str]] = None

class ScenarioPrice(BaseModel):
    price_per_kg: float
    total_revenue_inr: float
    estimated_expenses_inr: float
    net_profit_inr: float
    roi_percentage: float

class CropRecommendation(BaseModel):
    crop_id: str
    crop_name: str
    crop_name_ta: str
    category: str
    suitability_score: float # 0 to 100
    suitability_level: str # Highly Suitable, Moderately Suitable, Marginally Suitable
    growth_duration_days: int
    expected_harvest_date: date
    expected_yield_kg: float
    water_requirement_mm: float
    estimated_cultivation_cost_inr: float
    
    # 3 Forward Price Scenarios at Harvest Time
    pessimistic_scenario: ScenarioPrice
    normal_scenario: ScenarioPrice
    optimistic_scenario: ScenarioPrice
    
    confidence_score: float # 0.0 to 1.0
    key_risks: List[str]
    key_risks_ta: List[str]
    applicable_subsidies: List[str]
    data_sources: List[str]
    last_data_updated: str

class CropComparisonResponse(BaseModel):
    farmer_district: str
    area_acres: float
    recommendations: List[CropRecommendation]
    summary_advisory: str
    summary_advisory_ta: str

# --- Module B: Protect Schemas ---
class WeatherAlert(BaseModel):
    severity: str # low, medium, high, critical
    alert_type: str
    title: str
    title_ta: str
    description: str
    description_ta: str
    action_plan: str
    action_plan_ta: str
    source_agency: str
    valid_until: datetime

class CropStageAdvisory(BaseModel):
    crop_name: str
    crop_name_ta: str
    current_stage: str
    days_after_sowing: int
    irrigation_guidance: str
    irrigation_guidance_ta: str
    nutrient_management: str
    nutrient_management_ta: str
    pest_disease_watch: str
    pest_disease_watch_ta: str

class ProtectDashboardResponse(BaseModel):
    location: str
    current_temperature_c: float
    current_humidity_pct: float
    precipitation_next_24h_mm: float
    soil_moisture_index: str
    active_alerts: List[WeatherAlert]
    stage_advisories: List[CropStageAdvisory]

# --- Module C: Recover Schemas ---
class DisasterReportCreate(BaseModel):
    crop_cycle_id: str
    crop_name: str
    disaster_type: str
    incident_date: date
    affected_area_acres: float
    estimated_damage_percentage: float
    photos: List[str] = []
    notes: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class DisasterReportResponse(BaseModel):
    report_id: str
    crop_name: str
    incident_date: date
    is_within_72h_pmfby: bool
    hours_remaining_for_pmfby: float
    urgency_status: str
    claim_dossier_ready: bool
    sdrf_estimated_relief_inr: float
    pmfby_helpline: str
    official_action_checklist: List[str]
    official_action_checklist_ta: List[str]

# --- Module D: Reconnect Schemas ---
class ProduceListingCreate(BaseModel):
    crop_name: str
    crop_name_ta: str
    district: str
    quantity_kg: float
    quality_grade: str # grade_b_processing, grade_c_feed
    harvest_date: date
    shelf_life_days: int
    min_expected_price_per_kg: float
    safety_certified_non_rotten: bool
    photo_url: Optional[str] = None

class BuyerQuotationResponse(BaseModel):
    quotation_id: str
    buyer_name: str
    buyer_category: str
    is_verified: bool
    offered_price_per_kg: float
    procurement_terms: str
    transport_deduction_per_kg: float
    net_realization_per_kg: float
    total_net_payout_inr: float
    valid_until_hours: int

class ProduceListingResponse(BaseModel):
    listing_id: str
    crop_name: str
    crop_name_ta: str
    district: str
    quantity_kg: float
    quality_grade: str
    safety_status: str
    matching_buyers_count: int
    quotations: List[BuyerQuotationResponse]

# --- Offline Sync Schemas ---
class SyncMutationItem(BaseModel):
    client_mutation_id: str
    entity_type: str
    operation: str
    payload: Dict[str, Any]
    client_timestamp: datetime

class SyncPushRequest(BaseModel):
    device_id: str
    mutations: List[SyncMutationItem]

class SyncPushResponse(BaseModel):
    processed_count: int
    acknowledged_mutation_ids: List[str]
    server_time: datetime
