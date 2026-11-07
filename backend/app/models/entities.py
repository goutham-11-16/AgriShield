import uuid
from datetime import datetime, date
from sqlalchemy import (
    Column, String, Boolean, Integer, Float, Date, DateTime, Text, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
import enum
from backend.app.db.session import Base

class UserRole(str, enum.Enum):
    FARMER = "farmer"
    BUYER = "buyer"
    FPO_OFFICER = "fpo_officer"
    ADMIN = "admin"

class SoilType(str, enum.Enum):
    RED_SANDY_LOAM = "Red Sandy Loam"
    BLACK_COTTON = "Black Cotton"
    CLAYEY = "Clayey"
    ALLUVIAL = "Alluvial"
    RED_LOAM = "Red Loam"

class IrrigationType(str, enum.Enum):
    DRIP = "drip"
    SPRINKLER = "sprinkler"
    FLOOD = "flood"
    RAINFED = "rainfed"

class WaterSource(str, enum.Enum):
    BOREWELL = "borewell"
    OPEN_WELL = "open_well"
    CANAL = "canal"
    TANK = "tank"
    NONE = "none"

class DisasterType(str, enum.Enum):
    CYCLONE = "cyclone"
    FLOOD = "flood"
    DROUGHT = "drought"
    PEST_ATTACK = "pest_attack"
    HAILSTORM = "hailstorm"

class QualityGrade(str, enum.Enum):
    GRADE_A_RETAIL = "grade_a_retail"
    GRADE_B_PROCESSING = "grade_b_processing"
    GRADE_C_FEED = "grade_c_feed"
    UNSAFE_ROTTEN = "unsafe_rotten"

class QuotationStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    phone_number = Column(String(15), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), default=UserRole.FARMER.value)
    preferred_language = Column(String(10), default="ta")
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    farmer_profile = relationship("FarmerProfile", back_populates="user", uselist=False)
    buyer_profile = relationship("BuyerProfile", back_populates="user", uselist=False)

class FarmerProfile(Base):
    __tablename__ = "farmer_profiles"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    state = Column(String(50), default="Tamil Nadu")
    district = Column(String(50), nullable=False, index=True)
    block = Column(String(50), nullable=False)
    village = Column(String(50), nullable=False)
    fpo_membership_id = Column(String(50), nullable=True)
    pm_kisan_id = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="farmer_profile")
    farms = relationship("Farm", back_populates="farmer")

class Farm(Base):
    __tablename__ = "farms"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    farmer_id = Column(String(36), ForeignKey("farmer_profiles.id"), nullable=False)
    farm_name = Column(String(100), default="Main Plot")
    area_acres = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    soil_type = Column(String(50), default=SoilType.RED_SANDY_LOAM.value)
    irrigation_type = Column(String(20), default=IrrigationType.DRIP.value)
    water_source = Column(String(20), default=WaterSource.BOREWELL.value)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    farmer = relationship("FarmerProfile", back_populates="farms")
    crop_cycles = relationship("CropCycle", back_populates="farm")

class Crop(Base):
    __tablename__ = "crops"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    crop_name = Column(String(100), unique=True, nullable=False)
    crop_name_ta = Column(String(100), nullable=False)
    scientific_name = Column(String(100), nullable=True)
    category = Column(String(50), default="Vegetable")
    growth_duration_days = Column(Integer, nullable=False)
    water_requirement_mm = Column(Float, nullable=False)
    ideal_soil_ph_min = Column(Float, default=6.0)
    ideal_soil_ph_max = Column(Float, default=7.5)
    average_yield_per_acre_kg = Column(Float, nullable=False)
    average_cost_per_acre = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class CropCycle(Base):
    __tablename__ = "crop_cycles"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    farm_id = Column(String(36), ForeignKey("farms.id"), nullable=False)
    crop_id = Column(String(36), ForeignKey("crops.id"), nullable=False)
    sowing_date = Column(Date, nullable=False)
    expected_harvest_date = Column(Date, nullable=False)
    allocated_acres = Column(Float, nullable=False)
    status = Column(String(30), default="vegetative")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    farm = relationship("Farm", back_populates="crop_cycles")
    crop = relationship("Crop")
    risk_alerts = relationship("RiskAlert", back_populates="crop_cycle")
    disaster_reports = relationship("DisasterReport", back_populates="crop_cycle")

class MandiPrice(Base):
    __tablename__ = "mandi_prices"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    crop_id = Column(String(36), ForeignKey("crops.id"), nullable=False)
    state = Column(String(50), default="Tamil Nadu")
    district = Column(String(50), nullable=False)
    market_name = Column(String(100), nullable=False)
    variety = Column(String(50), default="Standard")
    arrival_date = Column(Date, nullable=False, index=True)
    min_price_per_quintal = Column(Float, nullable=False)
    max_price_per_quintal = Column(Float, nullable=False)
    modal_price_per_quintal = Column(Float, nullable=False)
    source = Column(String(50), default="AGMARKNET / data.gov.in")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    crop = relationship("Crop")

class RiskAlert(Base):
    __tablename__ = "risk_alerts"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    crop_cycle_id = Column(String(36), ForeignKey("crop_cycles.id"), nullable=False)
    severity = Column(String(20), default="medium") # low, medium, high, critical
    alert_type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    title_ta = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    description_ta = Column(Text, nullable=False)
    action_plan = Column(Text, nullable=False)
    action_plan_ta = Column(Text, nullable=False)
    source_model = Column(String(50), default="Open-Meteo & Agronomic Rules")
    is_acknowledged = Column(Boolean, default=False)
    valid_until = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    crop_cycle = relationship("CropCycle", back_populates="risk_alerts")

class DisasterReport(Base):
    __tablename__ = "disaster_reports"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    crop_cycle_id = Column(String(36), ForeignKey("crop_cycles.id"), nullable=False)
    disaster_type = Column(String(50), nullable=False)
    incident_date = Column(Date, nullable=False)
    affected_area_acres = Column(Float, nullable=False)
    estimated_damage_percentage = Column(Float, nullable=False)
    photos = Column(Text, default="[]") # JSON encoded list of paths/URLs
    notes = Column(Text, nullable=True)
    is_within_72h_pmfby = Column(Boolean, default=True)
    status = Column(String(30), default="submitted") # submitted, verified_by_fpo, resolved
    created_at = Column(DateTime, default=datetime.utcnow)
    
    crop_cycle = relationship("CropCycle", back_populates="disaster_reports")
    insurance_claim = relationship("InsuranceClaim", back_populates="disaster_report", uselist=False)

class InsuranceClaim(Base):
    __tablename__ = "insurance_claims"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    disaster_report_id = Column(String(36), ForeignKey("disaster_reports.id"), unique=True, nullable=False)
    scheme_type = Column(String(50), default="PMFBY")
    official_helpline = Column(String(50), default="14447")
    official_portal_url = Column(String(255), default="https://pmfby.gov.in/")
    claim_status = Column(String(50), default="dossier_generated")
    dossier_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    disaster_report = relationship("DisasterReport", back_populates="insurance_claim")

class ProduceListing(Base):
    __tablename__ = "produce_listings"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    crop_name = Column(String(100), nullable=False)
    crop_name_ta = Column(String(100), nullable=False)
    district = Column(String(50), nullable=False)
    quantity_kg = Column(Float, nullable=False)
    quality_grade = Column(String(50), default=QualityGrade.GRADE_B_PROCESSING.value)
    harvest_date = Column(Date, nullable=False)
    shelf_life_days = Column(Integer, default=5)
    min_expected_price_per_kg = Column(Float, nullable=False)
    photo_url = Column(String(255), nullable=True)
    safety_certified_non_rotten = Column(Boolean, default=True)
    status = Column(String(30), default="available") # available, quoted, sold
    created_at = Column(DateTime, default=datetime.utcnow)
    
    quotations = relationship("BuyerQuotation", back_populates="listing")

class BuyerProfile(Base):
    __tablename__ = "buyer_profiles"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    business_name = Column(String(150), nullable=False)
    buyer_category = Column(String(50), default="pulp_puree")
    gstin = Column(String(15), nullable=True)
    fssai_license = Column(String(20), nullable=True)
    operating_districts = Column(String(255), default="Dindigul,Coimbatore,Madurai,Theni")
    is_verified = Column(Boolean, default=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="buyer_profile")
    quotations = relationship("BuyerQuotation", back_populates="buyer")

class BuyerQuotation(Base):
    __tablename__ = "buyer_quotations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    produce_listing_id = Column(String(36), ForeignKey("produce_listings.id"), nullable=False)
    buyer_id = Column(String(36), ForeignKey("buyer_profiles.id"), nullable=False)
    offered_price_per_kg = Column(Float, nullable=False)
    procurement_terms = Column(String(50), default="farmgate_pickup") # farmgate_pickup, factory_delivery
    transport_cost_per_kg = Column(Float, default=1.20)
    net_realization_per_kg = Column(Float, nullable=False)
    valid_hours = Column(Integer, default=48)
    status = Column(String(30), default=QuotationStatus.PENDING.value)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    listing = relationship("ProduceListing", back_populates="quotations")
    buyer = relationship("BuyerProfile", back_populates="quotations")

class OfflineSyncQueue(Base):
    __tablename__ = "offline_sync_queue"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_mutation_id = Column(String(64), unique=True, nullable=False)
    entity_type = Column(String(50), nullable=False)
    operation = Column(String(20), nullable=False) # CREATE, UPDATE
    payload_json = Column(Text, nullable=False)
    synced_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
