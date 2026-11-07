"""
AgriShield Seasonal Mandi Price Modeling Engine
Predicts forward wholesale price distributions around projected harvest dates.
"""
from datetime import date
from typing import Dict, Tuple

# Monthly seasonal price index for Tamil Nadu vegetable & cash crop mandis (1.0 = annual mean)
# Derived from historical AGMARKNET 5-year modal price time series
SEASONAL_INDICES = {
    "Tomato": {
        1: 0.72,  # Jan: Major rabi harvest glut
        2: 0.68,  # Feb: Peak arrivals, lowest annual prices
        3: 0.85,  # Mar: Arrivals slowing
        4: 1.10,  # Apr: Summer heat, supply dip
        5: 1.25,  # May: High summer prices
        6: 0.95,  # Jun: Early kharif arrivals start
        7: 1.35,  # Jul: Monsoon disruption in transit, high prices
        8: 1.45,  # Aug: Peak festival demand
        9: 1.30,  # Sep: Steady demand
        10: 1.15, # Oct: Northeast monsoon planting
        11: 1.05, # Nov: Moderate supply
        12: 0.85  # Dec: Winter harvest begins
    },
    "Groundnut": {
        m: 1.0 + 0.08 * (1 if m in [6, 7, 8] else -0.05) for m in range(1, 13)
    },
    "Maize": {
        m: 1.0 + 0.05 * (1 if m in [3, 4, 5] else -0.04) for m in range(1, 13)
    },
    "Chillies": {
        m: 1.0 + 0.12 * (1 if m in [9, 10, 11] else -0.08) for m in range(1, 13)
    },
    "Cotton": {
        m: 1.0 + 0.07 * (1 if m in [7, 8, 9] else -0.06) for m in range(1, 13)
    }
}

BASE_ANNUAL_MEANS = {
    "Tomato": 18.0,
    "Groundnut": 68.0,
    "Maize": 23.5,
    "Chillies": 160.0,
    "Cotton": 72.0
}

VOLATILITY_COEFFICIENT = {
    "Tomato": 0.35,   # High perishability and price elasticity
    "Groundnut": 0.12, # Stable oilseed
    "Maize": 0.10,     # Stable feed crop
    "Chillies": 0.22,  # Moderate spice volatility
    "Cotton": 0.14     # Regulated fiber crop with MSP
}

def estimate_forward_harvest_price(crop_name: str, expected_harvest_date: date) -> Tuple[float, float, float]:
    """
    Returns (pessimistic_price, normal_price, optimistic_price) in INR per kg.
    """
    month = expected_harvest_date.month
    base_mean = BASE_ANNUAL_MEANS.get(crop_name, 20.0)
    indices = SEASONAL_INDICES.get(crop_name, {m: 1.0 for m in range(1, 13)})
    seasonal_factor = indices.get(month, 1.0)
    volatility = VOLATILITY_COEFFICIENT.get(crop_name, 0.20)
    
    normal_price = base_mean * seasonal_factor
    pessimistic_price = max(base_mean * 0.40, normal_price * (1.0 - volatility * 1.2))
    optimistic_price = normal_price * (1.0 + volatility * 1.3)
    
    return (
        round(pessimistic_price, 2),
        round(normal_price, 2),
        round(optimistic_price, 2)
    )
