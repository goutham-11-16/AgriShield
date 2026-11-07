from datetime import date, datetime
from typing import List, Dict, Any
import uuid
from backend.app.schemas.schemas import (
    ProduceListingCreate, ProduceListingResponse, BuyerQuotationResponse
)

# Verified industrial agro-processing buyers in Tamil Nadu food processing corridors
VERIFIED_BUYERS = [
    {
        "buyer_id": "buyer_tn_pulp_01",
        "business_name": "Nilakottai Agro-Foods & Puree Processing Ltd",
        "category": "Tomato Pulp & Puree Manufacturer",
        "gstin": "33AABCN1234F1Z9",
        "district": "Dindigul",
        "base_offered_price_per_kg": 11.50,
        "transport_cost_per_kg": 1.20,
        "procurement_terms": "Factory Gate Delivery (Dindigul Food Park)",
        "valid_hours": 48
    },
    {
        "buyer_id": "buyer_tn_sauce_02",
        "business_name": "Kaveri Valley Natural Condiments & Sauces",
        "category": "Sauce & Pickle Manufacturer",
        "gstin": "33AACCK9876G2Z1",
        "district": "Coimbatore",
        "base_offered_price_per_kg": 10.80,
        "transport_cost_per_kg": 0.00, # Farmgate direct pickup by buyer vehicle
        "procurement_terms": "Farmgate Pickup (Buyer Logistics Provided)",
        "valid_hours": 36
    },
    {
        "buyer_id": "buyer_tn_feed_03",
        "business_name": "Madurai Bio-Enrich Cattle & Poultry Feed",
        "category": "Livestock Feed Compounder",
        "gstin": "33AAEFM5544H3Z5",
        "district": "Madurai",
        "base_offered_price_per_kg": 5.50,
        "transport_cost_per_kg": 0.80,
        "procurement_terms": "Farmgate Bulk Pickup",
        "valid_hours": 24
    }
]

def evaluate_and_match_produce(listing: ProduceListingCreate) -> ProduceListingResponse:
    listing_id = f"LIST-{str(uuid.uuid4())[:8].upper()}"
    
    # 1. Critical Safety Check
    if not listing.safety_certified_non_rotten or listing.quality_grade == "unsafe_rotten":
        return ProduceListingResponse(
            listing_id=listing_id,
            crop_name=listing.crop_name,
            crop_name_ta=listing.crop_name_ta,
            district=listing.district,
            quantity_kg=listing.quantity_kg,
            quality_grade="unsafe_rotten",
            safety_status="REJECTED - Fungal/Bacterial Decay Detected. Unsafe for food or animal consumption.",
            matching_buyers_count=0,
            quotations=[]
        )
        
    matching_quotes: List[BuyerQuotationResponse] = []
    
    for b in VERIFIED_BUYERS:
        # Match buyers based on grade
        if listing.quality_grade == "grade_b_processing" and "Feed" in b["category"]:
            continue # Prefer higher-value puree/sauce buyers for Grade B
        if listing.quality_grade == "grade_c_feed" and "Puree" in b["category"]:
            continue # Puree processors cannot accept Grade C
            
        offered = b["base_offered_price_per_kg"]
        transport = b["transport_cost_per_kg"]
        net_price = max(0.0, round(offered - transport, 2))
        total_payout = round(listing.quantity_kg * net_price, 2)
        
        quote = BuyerQuotationResponse(
            quotation_id=f"QUO-{str(uuid.uuid4())[:8].upper()}",
            buyer_name=b["business_name"],
            buyer_category=b["category"],
            is_verified=True,
            offered_price_per_kg=round(offered, 2),
            procurement_terms=b["procurement_terms"],
            transport_deduction_per_kg=round(transport, 2),
            net_realization_per_kg=net_price,
            total_net_payout_inr=total_payout,
            valid_until_hours=b["valid_hours"]
        )
        matching_quotes.append(quote)
        
    # Sort quotes by net realization descending
    matching_quotes.sort(key=lambda x: x.net_realization_per_kg, reverse=True)
    
    return ProduceListingResponse(
        listing_id=listing_id,
        crop_name=listing.crop_name,
        crop_name_ta=listing.crop_name_ta,
        district=listing.district,
        quantity_kg=listing.quantity_kg,
        quality_grade=listing.quality_grade,
        safety_status="VERIFIED POTENTIALLY USABLE - Visual check passed. Suitable for industrial processing.",
        matching_buyers_count=len(matching_quotes),
        quotations=matching_quotes
    )
