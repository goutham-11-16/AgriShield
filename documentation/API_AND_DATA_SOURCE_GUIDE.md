# AgriShield: Comprehensive API & Agricultural Data Source Audit Guide

**Document Version:** 1.0.0  
**Target Region:** India (Primary Pilot: Tamil Nadu)  
**Date:** November 2026  

---

## 1. Executive Summary & Source Status Matrix

The following table categorizes every external data source evaluated for the four AgriShield modules:
- **Module A (Predict):** Crop suitability, soil health, historical mandi trends, forward harvest price ranges.
- **Module B (Prepare & Protect):** Weather forecasts, extreme agro-weather alerts, stage-specific advisories, pest/disease tracking.
- **Module C (Recover):** Disaster reporting, PMFBY claim guidance, SDRF/NDRF relief, loss evidence organization.
- **Module D (Reconnect):** Distressed produce listing, industrial/processing buyer discovery, quotation matching, net realization calculation.

### Master Data Source Status Table

| Data Requirement | Provider / System | Official API? | API Key? | Cost / Access | Current Status | Integration Approach in AgriShield |
|---|---|---|---|---|---|---|
| **Daily Mandi Prices & Arrivals** | Open Government Data (data.gov.in) / AGMARKNET | Yes (REST JSON) | Yes | Free (Govt registration) | **Public but needs registration** | Direct ingestion via OGD API endpoint `resource/9ef84268-d588-465a-a308-a864a43d0070` with local SQLite/PostgreSQL caching. |
| **Real-time & Forecast Agro-Weather** | Open-Meteo (open-meteo.com) | Yes (REST JSON) | No (Free tier) | Free for non-commercial (<10k/day) | **Verified and accessible** | Direct API querying for 7-day hourly temperature, precipitation, soil moisture (0-7cm), and ET0. |
| **Historical Climate & Solar Radiation** | NASA POWER (power.larc.nasa.gov) | Yes (REST JSON) | No | Free (Open public) | **Verified and accessible** | Ingestion pipeline for daily historical rainfall and solar radiation (T2M, PRECTOTCORR, ALLSKY_SFC_SW_DWN) to compute crop GDD and yield baseline. |
| **National Weather Warnings & Cyclones** | India Meteorological Department (IMD / Mausam) | No public open REST API | N/A | Free public web / CAP feeds | **Download-only / RSS Feed** | Ingestion of IMD Common Alerting Protocol (CAP) RSS feeds + District Agro-Met Bulletins (DAMU/GKMS) parsed via scheduled pipeline. |
| **Mandi E-Trading & Logistics** | e-NAM (enam.gov.in) | No public open 3rd-party API | N/A | Restricted to registered APMCs/traders | **No public API found** | Fallback to data.gov.in AGMARKNET daily arrivals & mandi modal price time-series; portal deep-links for APMC e-trading. |
| **Soil Macro & Micro Nutrients** | Soil Health Card Portal (soilhealth.dac.gov.in) | No public open developer API | N/A | Restricted (Official dept login) | **Download-only** | Curated district/block baseline soil fertility tables (N, P, K, pH, EC, Organic Carbon) from state soil reports + manual farmer report input. |
| **Satellite Land Use & Indices** | ISRO Bhuvan (bhuvan.nrsc.gov.in) | Yes (WMS/WFS map services) | Yes (Token) | Free after portal registration | **Public but needs registration** | Leaflet/MapLibre WMS overlay for regional agro-ecological zones and vegetation index; Sentinel-2 open fallback. |
| **Groundwater Levels & Aquifers** | Central Ground Water Board / India-WRIS (indiawris.gov.in) | Semi-open (GIS REST/WFS) | No / Session | Free public data | **Download-only** | Pre-compiled district aquifer recharge and seasonal block water table status; fallback to farmer irrigation source interview. |
| **Crop Packages of Practices & Calendars** | TNAU Agritech Portal (agritech.tnau.ac.in) & ICAR | No public REST API | N/A | Free public domain knowledge | **Download-only** | Structured agronomic knowledge base (crop stages, thermal units, water requirements, pest thresholds) curated into reproducible seed files. |
| **Crop Insurance (PMFBY)** | Pradhan Mantri Fasal Bima Yojana (pmfby.gov.in) | Restricted to Banks/Insurers | Restricted | Govt Institutional Only | **Requires approval** | Rule-engine guided workflow (72h local calamity deadline, required documents, 14447 helpline, insurance company directory, loss claim dossier generator). |
| **State Disaster Relief (SDRF/NDRF)** | TN Agrisnet & Revenue Administration (CRA TN) | No public REST API | N/A | Free public portal | **No public API found** | Official SDRF norm calculator based on land classification (rainfed vs irrigated), compensation guidelines, and e-Sevaimaiyam links. |
| **Indic Languages & Voice** | Bhashini / AI4Bharat (bhashini.gov.in / IIT Madras) | Yes (REST) | Yes (ULCA API Key) | Free for public good / R&D | **Public but needs registration** | Bhashini ASR/TTS API integration with Android on-device SpeechRecognizer and TTS as zero-latency offline fallback. |

---

## 2. In-Depth Source Audit Profiles

### A. Open Government Data Platform (data.gov.in) - Mandi Prices & Arrivals

1. **Official Website:** `https://www.data.gov.in/`
2. **Official API Documentation:** `https://www.data.gov.in/help/apis`
3. **Direct Registration URL:** `https://www.data.gov.in/user/register`
4. **Account Creation:**
   - Go to `https://www.data.gov.in/user/register`.
   - Fill in Full Name, Email Address, Mobile Number, and Organization Type (Individual, Student, Academic, Commercial).
   - Verify mobile OTP and email verification link.
5. **How to Request API Access:**
   - Log in to your account at `https://www.data.gov.in/user/login`.
   - Navigate to "My Account" -> "API Key Management".
   - Click "Generate New API Key".
6. **API Key Required:** Yes (`api-key` query parameter).
7. **Where Key is Obtained:** Account Dashboard under "My API Key".
8. **Approval Required:** Automatic upon email/mobile verification.
9. **Cost & Licensing:** Free of cost under the National Data Sharing and Accessibility Policy (NDSAP).
10. **Rate Limits & Restrictions:** Maximum 10,000 requests per day per API key; max limit per request = 1000 records.
11. **Authentication Method:** Query parameter `api-key=<YOUR_KEY>`.
12. **Sample API Request:**
    ```bash
    curl -X GET "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=YOUR_API_KEY&format=json&offset=0&limit=5&filters[state]=Tamil+Nadu&filters[commodity]=Tomato"
    ```
13. **Sample API Response:**
    ```json
    {
      "index_name": "9ef84268-d588-465a-a308-a864a43d0070",
      "title": "Daily Mandi Prices and Arrivals",
      "desc": "Wholesale prices and arrivals of agricultural commodities",
      "records": [
        {
          "state": "Tamil Nadu",
          "district": "Dindigul",
          "market": "Oddanchatram",
          "commodity": "Tomato",
          "variety": "Hybrid",
          "arrival_date": "07/11/2026",
          "min_price": "1400",
          "max_price": "2200",
          "modal_price": "1800"
        }
      ],
      "total": 1
    }
    ```
14. **Integration Feasibility:** High. Can be queried daily via background worker and cached in PostgreSQL/SQLite.
15. **Alternative if Unavailable:** Pre-computed 5-year seasonal price indices curated from historical AGMARKNET annual bulletin tables.

---

### B. Open-Meteo Agro-Weather API

1. **Official Website:** `https://open-meteo.com/`
2. **Official API Documentation:** `https://open-meteo.com/en/docs`
3. **Direct Registration URL:** Not required for standard free tier. For commercial keys: `https://open-meteo.com/en/pricing`
4. **Account Creation:** Immediate access without login for up to 10,000 daily calls.
5. **How to Request API Access:** Direct GET requests to endpoints; commercial users register with billing.
6. **API Key Required:** No for non-commercial (<10,000 calls/day); Yes for commercial.
7. **Where Key is Obtained:** Not applicable for standard open usage.
8. **Approval Required:** None.
9. **Cost & Licensing:** Free for non-commercial under CC BY 4.0; Commercial plans start at €19/month.
10. **Rate Limits:** Free tier: 10,000 daily calls, max 60 calls/minute.
11. **Authentication Method:** None required (URL parameter `apikey` for commercial).
12. **Sample API Request:**
    ```bash
    curl -s "https://api.open-meteo.com/v1/forecast?latitude=11.1271&longitude=78.6569&current=temperature_2m,relative_humidity_2m,precipitation,weather_code&hourly=temperature_2m,precipitation_probability,soil_temperature_0cm,soil_moisture_0_to_1cm&timezone=Asia%2FKolkata&forecast_days=7"
    ```
13. **Sample API Response:**
    ```json
    {
      "latitude": 11.14,
      "longitude": 78.65,
      "current": {
        "temperature_2m": 28.4,
        "relative_humidity_2m": 72,
        "precipitation": 0.0,
        "weather_code": 1
      },
      "hourly": {
        "time": ["2026-11-07T00:00", "2026-11-07T01:00"],
        "temperature_2m": [24.2, 23.8],
        "soil_moisture_0_to_1cm": [0.28, 0.28]
      }
    }
    ```
14. **Integration Feasibility:** Immediate and tested. Fully verified live.
15. **Alternative if Unavailable:** NASA POWER daily API or IMD daily bulletin parsing.

---

### C. NASA POWER (Prediction Of Worldwide Energy Resources)

1. **Official Website:** `https://power.larc.nasa.gov/`
2. **Official API Documentation:** `https://power.larc.nasa.gov/docs/services/api/`
3. **Direct Registration URL:** No registration required. Open Public API.
4. **Account Creation:** None needed.
5. **How to Request Access:** Direct HTTPS queries.
6. **API Key Required:** No.
7. **Where Key is Obtained:** Public.
8. **Approval Required:** None.
9. **Cost & Licensing:** Free open public data provided by NASA Earth Science Division.
10. **Rate Limits:** 30 requests per minute recommended to ensure service stability.
11. **Authentication Method:** None.
12. **Sample API Request:**
    ```bash
    curl -s "https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN&community=AG&longitude=78.65&latitude=11.12&start=20240101&end=20240105&format=JSON"
    ```
13. **Sample API Response:**
    ```json
    {
      "type": "Feature",
      "properties": {
        "parameter": {
          "T2M": {"20240101": 24.19, "20240102": 24.13},
          "PRECTOTCORR": {"20240101": 0.0, "20240102": 0.0},
          "ALLSKY_SFC_SW_DWN": {"20240101": 18.2, "20240102": 17.9}
        }
      }
    }
    ```
14. **Integration Feasibility:** Immediate and verified live.
15. **Alternative if Unavailable:** ECMWF ERA5 reanalysis or Open-Meteo Historical Weather API.

---

### D. India Meteorological Department (IMD) - Mausam & Agrimet

1. **Official Website:** `https://mausam.imd.gov.in/` | `https://imdagrimet.gov.in/`
2. **Official API Documentation:** No public developer REST API documentation exists for direct third-party developers without a signed institutional MoU with Ministry of Earth Sciences.
3. **Direct Registration URL:** N/A for public API.
4. **Account Creation:** Restricted to government agencies, aviation, and research institutions.
5. **How to Request Access:** Formal request to Director General of Meteorology, IMD, Lodhi Road, New Delhi.
6. **API Key Required:** Institutional MoU / IP whitelisting.
7. **Where Key is Obtained:** IMD IT division.
8. **Approval Required:** Yes, formal ministry approval.
9. **Cost & Licensing:** Public weather forecasts are free for general public view; automated data feeds for commercial apps require commercial licensing and data dissemination charges.
10. **Rate Limits:** Defined per institutional agreement.
11. **Authentication Method:** VPN / IP whitelist / Basic auth for authorized servers.
12. **Sample Public Resource:** CAP (Common Alerting Protocol) RSS feeds published via `https://mausam.imd.gov.in/responsive/all_india_warning_rss.php`.
13. **Integration Feasibility:** Feasible via CAP RSS XML parsing for cyclone/heavy rainfall alert polygons, combined with GKMS Agromet Advisory bulletins.
14. **Alternative if Unavailable:** Open-Meteo weather code thresholds + WMO Severe Weather Information Centre (SWIC).

---

### E. Pradhan Mantri Fasal Bima Yojana (PMFBY)

1. **Official Website:** `https://pmfby.gov.in/`
2. **Official API Documentation:** Restricted National Crop Insurance Portal (NCIP) API documentation. Not public.
3. **Direct Registration URL:** `https://pmfby.gov.in/` (Farmer registration portal for claims & enrollment).
4. **Account Creation:** Farmers create individual accounts using Aadhaar and mobile OTP.
5. **API Access Request:** NCIP APIs are strictly limited to scheduled commercial banks, CSC e-Governance Services, and empaneled general insurance companies (AIC, HDFC ERGO, ICICI Lombard, etc.).
6. **API Key Required:** Mutual TLS certificates + JWT tokens issued by Dept of Agriculture & Farmers Welfare (DA&FW).
7. **Approval Required:** High-level statutory clearance.
8. **Cost & Licensing:** Zero cost for authorized financial and public entities; closed to external consumer apps.
9. **Integration Feasibility:** AgriShield implements the **Official Assisted Workflow & Dossier Generator**:
   - Collects farmer evidence, geolocated photos, date of loss, crop stage.
   - Calculates time remaining against the mandatory **72-hour Local Calamity Reporting Rule**.
   - Generates the standard PMFBY Loss Notification Sheet PDF ready to hand to the local Agriculture Officer / Bank Branch / Insurance Representative.
   - Direct-dials PMFBY National Toll-Free Helpline: **14447** / **1800 180 1551**.
   - Directs farmer to official claim portal `https://pmfby.gov.in/farmerRegistrationForm`.

---

### F. Soil Health Card & Digital Soil Data

1. **Official Website:** `https://soilhealth.dac.gov.in/`
2. **Official API Documentation:** None public.
3. **Account Creation:** District laboratory and state agriculture department personnel only.
4. **Integration Approach:**
   - AgriShield includes a standardized **Tamil Nadu District Soil Nutrient Matrix** (covering all 38 districts including Dindigul, Thanjavur, Coimbatore, Madurai, Tiruchirappalli) calibrated against published ICAR and TNAU Soil Science benchmarks (Available Nitrogen, Available Phosphorus, Available Potassium, pH, Electrical Conductivity, Micronutrients: Zinc, Boron, Iron).
   - Allows farmers to optionally input their individual SHC 12-parameter lab values when available.

---

### G. Indic Voice & Language Translation (Bhashini / AI4Bharat)

1. **Official Website:** `https://bhashini.gov.in/` | `https://ai4bharat.iitm.ac.in/`
2. **API Documentation:** `https://bhashini.gitbook.io/bhashini-apis/`
3. **Direct Registration:** `https://bhashini.gov.in/en/join-ecosystem`
4. **Account Creation:** Register organization / developer profile on Universal Language Contribution API (ULCA).
5. **API Key Required:** Yes (`apiKey` and `userId` header).
6. **Approval Required:** Email verification and platform moderation.
7. **Cost & Licensing:** Free for Indian digital public goods and academic innovation.
8. **Integration Feasibility:** Direct REST API integration for server-side translation; Android native `android.speech.SpeechRecognizer` and `android.speech.tts.TextToSpeech` as resilient zero-latency offline fallback.

---

## 3. Technology Stack Justification

- **Backend:** Python FastAPI (asynchronous, high concurrency, OpenAPI/Swagger native documentation, seamless ML inference integration).
- **Database:** PostgreSQL with PostGIS extension for spatial queries (with SQLite/SpatiaLite fallback for zero-dependency local testing).
- **ML / Crop Modeling Engine:**
  - Scikit-learn & LightGBM for yield estimation.
  - Seasonal decomposition + SARIMAX/Holt-Winters for forward harvest price confidence intervals (Optimistic, Normal, Pessimistic).
  - Deterministic Agronomic Rules Engine based on ICAR/TNAU guidelines for water balance and crop duration.
- **Android App:** Kotlin + Jetpack Compose with Room Database (SQLite) for offline-first data persistence, WorkManager for idempotent background sync, and CameraX for disaster photo capture with embedded EXIF GPS tags.
- **Web Dashboard:** React + Vite + Tailwind CSS for FPOs, KVK scientists, and Agricultural Officers.

---

## 4. Realistic MVP Roadmap (Phase 0 to Phase 5)

1. **Phase 0:** Research, API Verification, and Data Pipeline Calibration (Completed).
2. **Phase 1 (MVP Core):** Farmer registration, farm profile, 3-crop comparison engine with forward price ranges, Tamil/English bilingual UI, offline caching.
3. **Phase 2 (Protect):** Weather forecasting, 7-day crop risk monitors, pest/disease advisories, local notifications.
4. **Phase 3 (Recover):** Geotagged damage reporting, 72-hour PMFBY countdown timer, claim dossier PDF generator, emergency relief directory.
5. **Phase 4 (Market Recovery):** Distressed/processing-grade produce listing (pulp, puree, sauce), verified buyer directory, net realization logistics calculator.
6. **Phase 5 (Field Validation):** Pilot evaluation with FPOs in Tamil Nadu (Dindigul tomato cluster).
