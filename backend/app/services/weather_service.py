import httpx
from datetime import datetime, timedelta
from typing import List, Optional
from backend.app.schemas.schemas import WeatherAlert, CropStageAdvisory, ProtectDashboardResponse

# Default coordinates for Tamil Nadu pilot district (Dindigul)
DEFAULT_LAT = 11.1271
DEFAULT_LON = 78.6569

async def fetch_weather_and_risks(
    lat: float = DEFAULT_LAT,
    lon: float = DEFAULT_LON,
    district_name: str = "Dindigul",
    crop_name: str = "Tomato",
    sowing_days_ago: int = 45
) -> ProtectDashboardResponse:
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&hourly=temperature_2m,precipitation_probability,precipitation,soil_moisture_0_to_1cm&timezone=Asia%2FKolkata&forecast_days=7"
    
    current_temp = 28.5
    current_humidity = 75.0
    rain_next_24h = 0.0
    wind_speed = 12.0
    
    try:
        async with httpx.AsyncClient(timeout=6.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                curr = data.get("current", {})
                current_temp = curr.get("temperature_2m", 28.5)
                current_humidity = curr.get("relative_humidity_2m", 75.0)
                wind_speed = curr.get("wind_speed_10m", 12.0)
                
                hourly = data.get("hourly", {})
                rain_series = hourly.get("precipitation", [])
                if rain_series:
                    rain_next_24h = sum(rain_series[:24])
    except Exception:
        # Fallback to local climatological baseline if offline or timeout
        pass

    alerts: List[WeatherAlert] = []
    
    # 1. Heavy Rain / Cyclone Detection
    if rain_next_24h > 45.0 or wind_speed > 40.0:
        alerts.append(WeatherAlert(
            severity="critical",
            alert_type="heavy_rainfall_cyclone",
            title="Heavy Rainfall & Strong Wind Advisory",
            title_ta="கனமழை மற்றும் பலத்த காற்று எச்சரிக்கை",
            description=f"Forecast indicates {rain_next_24h:.1f}mm rainfall with wind gusts up to {wind_speed:.1f} km/h over {district_name}.",
            description_ta=f"{district_name} பகுதியில் அடுத்த 24 மணி நேரத்தில் {rain_next_24h:.1f} மி.மீ மழை மற்றும் மணிக்கு {wind_speed:.1f} கி.மீ வேகத்தில் பலத்த காற்று வீசக்கூடும்.",
            action_plan="1. Clean and deepen drainage channels around field edges to avoid waterlogging.\n2. Provide staking support for tall vegetable crops (Tomato, Chillies).\n3. Postpone fertilizer top-dressing and pesticide spraying until rain subsides.",
            action_plan_ta="1. நிலத்தில் நீர் தேங்குவதைத் தவிர்க்க வரப்புகளில் உள்ள வடிகால் வாய்க்கால்களை தூர்வாரி தயார் செய்யவும்.\n2. தக்காளி, மிளகாய் போன்ற பயிர்களுக்கு மூங்கில் குச்சிகளால் முட்டுக் கொடுத்து பலப்படுத்தவும்.\n3. மழை நிற்கும் வரை உரமிடுதல் மற்றும் பூச்சிக்கொல்லி தெளிப்பதை உடனடியாக ஒத்திவைக்கவும்.",
            source_agency="Open-Meteo & IMD Agromet Bulletin",
            valid_until=datetime.utcnow() + timedelta(hours=48)
        ))
    else:
        # Preventative precautionary advisory
        alerts.append(WeatherAlert(
            severity="low",
            alert_type="moderate_weather",
            title="Stable Agro-Weather Conditions",
            title_ta="சீரான வானிலை சூழல்",
            description=f"Moderate conditions across {district_name}. Expected 24h precipitation: {rain_next_24h:.1f}mm.",
            description_ta=f"{district_name} பகுதியில் சீரான வானிலை நிலவுகிறது. எதிர்பார்க்கப்படும் 24 மணி நேர மழை அளவு: {rain_next_24h:.1f} மி.மீ.",
            action_plan="Continue routine intercultural operations and drip irrigation scheduling as per crop stage requirements.",
            action_plan_ta="பயிரின் வளர்ச்சிப் பருவத்திற்கு ஏற்ப வழக்கமான களையெடுத்தல் மற்றும் சொட்டுநீர்ப் பாசனத்தை தொடரலாம்.",
            source_agency="Open-Meteo Agro-Model",
            valid_until=datetime.utcnow() + timedelta(hours=24)
        ))
        
    # 2. Disease / Blight Alert for High Humidity
    if current_humidity > 70.0 and current_temp < 30.0:
        alerts.append(WeatherAlert(
            severity="high" if current_humidity > 85.0 else "medium",
            alert_type="fungal_blight_risk",
            title="Early / Late Blight Risk Warning",
            title_ta="இலைக்கருகல் நோய் தாக்கும் அபாய எச்சரிக்கை",
            description=f"Relative humidity at {current_humidity:.1f}% with mild temperatures creates ideal micro-climate for fungal spore multiplication in solanaceous crops.",
            description_ta=f"காற்றில் ஈரப்பதம் {current_humidity:.1f}% ஆகவும் மிதமான வெப்பநிலையும் நிலவுவதால், தக்காளி மற்றும் கத்தரி பயிர்களில் பூஞ்சான இலைக்கருகல் நோய் பரவும் சூழல் உருவாகியுள்ளது.",
            action_plan="Spray Pseudomonas fluorescens (0.2%) or Copper Hydroxide (2g/L) during morning hours. Ensure adequate leaf canopy aeration.",
            action_plan_ta="சூடோமோனாஸ் புளோரசன்ஸ் (Pseudomonas fluorescens) 0.2% அல்லது காப்பர் ஹைட்ராக்சைடு 2 கிராம்/லிட்டர் வீதம் காலை வேளையில் தெளிக்கவும். பயிரில் காற்று புகுமாறு பார்த்துக் கொள்ளவும்.",
            source_agency="TNAU Crop Protection Diagnostic Rules",
            valid_until=datetime.utcnow() + timedelta(hours=36)
        ))

    # Stage-specific advisory calculation
    stage = "Flowering & Fruit Set"
    stage_ta = "பூத்தல் மற்றும் காய் பிடிக்கும் பருவம்"
    if sowing_days_ago < 25:
        stage = "Vegetative / Seedling"
        stage_ta = "வளர்ச்சி / நாற்றுப் பருவம்"
    elif sowing_days_ago > 80:
        stage = "Maturity & Harvesting"
        stage_ta = "முதிர்ச்சி மற்றும் அறுவடைப் பருவம்"

    stage_advisories = [
        CropStageAdvisory(
            crop_name=crop_name,
            crop_name_ta="தக்காளி (Tomato)",
            current_stage=f"{stage} (Day {sowing_days_ago})",
            days_after_sowing=sowing_days_ago,
            irrigation_guidance="Maintain consistent soil moisture at 65-75% field capacity. Avoid water stress to prevent blossom end rot.",
            irrigation_guidance_ta="மண்ணில் 65-75% ஈரப்பதம் இருக்குமாறு சொட்டுநீர் பாசனம் செய்யவும். பூ உதிர்வதையும் காய் அழுகலையும் தடுக்க சீரான நீர் மேலாண்மை அவசியம்.",
            nutrient_management="Apply 13-0-45 (Potassium Nitrate) @ 2.5 kg/acre via fertigation to enhance fruit size, firmness and shelf-life.",
            nutrient_management_ta="காய்களின் பளபளப்பு மற்றும் திரட்சியை அதிகரிக்க 13-0-45 பொட்டாசியம் நைட்ரேட் உரத்தை ஏக்கருக்கு 2.5 கிலோ வீதம் பாசன நீரில் செலுத்தவும்.",
            pest_disease_watch="Inspect under-surface of leaves for whitefly and leaf miner trails. Install yellow sticky traps (10 per acre).",
            pest_disease_watch_ta="வெள்ளை ஈ மற்றும் இலைத்துளைப்பான் புழுக்கள் உள்ளதா என இலைகளின் அடிப்பகுதியை கண்காணிக்கவும். ஏக்கருக்கு 10 மஞ்சள் ஒட்டும் பொறிகளை வைக்கவும்."
        )
    ]

    return ProtectDashboardResponse(
        location=f"{district_name}, Tamil Nadu",
        current_temperature_c=round(current_temp, 1),
        current_humidity_pct=round(current_humidity, 1),
        precipitation_next_24h_mm=round(rain_next_24h, 1),
        soil_moisture_index="Adequate (0.28 m³/m³)",
        active_alerts=alerts,
        stage_advisories=stage_advisories
    )
