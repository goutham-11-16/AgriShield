"""
AgriShield Soil & Agronomic Suitability Engine
Scores multi-criteria fitness for crops based on soil, irrigation, and weather parameters.
"""
from typing import Dict, Any

SOIL_COMPATIBILITY_MATRIX = {
    "Red Sandy Loam": ["Tomato", "Groundnut", "Chillies", "Maize"],
    "Black Cotton": ["Cotton", "Chillies", "Tomato", "Maize"],
    "Red Loam": ["Tomato", "Groundnut", "Maize", "Chillies"],
    "Alluvial": ["Paddy", "Maize", "Groundnut", "Tomato"],
    "Clayey": ["Paddy", "Cotton"]
}

WATER_STRESS_TOLERANCE = {
    "Groundnut": 0.85, # Highly drought tolerant
    "Maize": 0.75,     # Moderately tolerant
    "Cotton": 0.70,    # Deep rooted
    "Chillies": 0.55,  # Moderate
    "Tomato": 0.40     # Shallow rooted, sensitive to water stress
}

def calculate_crop_fitness(
    crop_name: str,
    soil_type: str,
    irrigation_method: str,
    budget_available: float,
    cultivation_cost: float
) -> float:
    score = 0.0
    
    # 1. Soil compatibility
    compatible = SOIL_COMPATIBILITY_MATRIX.get(soil_type, [])
    if crop_name in compatible:
        score += 40.0
    else:
        score += 20.0
        
    # 2. Irrigation compatibility
    if irrigation_method == "drip":
        score += 35.0
    elif irrigation_method == "sprinkler":
        score += 30.0
    elif irrigation_method == "flood":
        score += 25.0
    elif irrigation_method == "rainfed":
        tolerance = WATER_STRESS_TOLERANCE.get(crop_name, 0.5)
        score += 35.0 * tolerance
        
    # 3. Budget feasibility
    if budget_available >= cultivation_cost:
        score += 25.0
    else:
        ratio = budget_available / cultivation_cost if cultivation_cost > 0 else 1.0
        score += 25.0 * min(1.0, max(0.2, ratio))
        
    return min(100.0, round(score, 1))
