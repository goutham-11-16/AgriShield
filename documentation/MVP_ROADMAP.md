# AgriShield - Product Roadmap (Phase 0 to Phase 5)

## Phase 0: Research, API Audit & Technical Feasibility (Done)
- Comprehensive audit of data.gov.in, Open-Meteo, NASA POWER, IMD CAP alerts, PMFBY.
- Architecture specification, database entity models, and offline sync protocol.
- Credential management structure (`.env.example`, `API_SETUP.md`).

## Phase 1: MVP Core - Crop Decision Engine (Module A)
- **Farmer & Farm Onboarding:** District, soil type, irrigation type, budget.
- **Crop Suitability Matrix:** Calibrated for Tamil Nadu crops (Tomato, Paddy, Cotton, Groundnut, Maize, Chillies).
- **Forward Price & Profit Range Estimator:**
  - Optimistic, Normal, and Pessimistic scenarios at predicted harvest date.
  - Multi-crop side-by-side comparison (3 crops).
- **Data Caching & Offline Baseline:** Local storage of historical prices and soil tables.
- **Localization:** Full Tamil (`ta`) and English (`en`) bilingual support.

## Phase 2: Weather & Crop Protection (Module B)
- 7-day localized agro-weather forecasts from Open-Meteo.
- Early warning threshold detector (cyclone, heavy rain >65mm, heatwave, blight humidity index).
- Stage-specific agro-advisories based on sowing date and crop duration.
- Push/local Android notifications with actionable protection steps.

## Phase 3: Disaster Recovery & PMFBY Dossier (Module C)
- Damage incident logging with geotagged photo capture.
- Automated PMFBY 72-hour reporting countdown timer.
- Standardized PMFBY Loss Notification Claim Dossier generator.
- State Disaster Response Fund (SDRF) relief calculator and helpline directory.

## Phase 4: Alternative Market Discovery & Salvage (Module D)
- Listing distressed/processing-grade produce (Grade B / Grade C).
- Verified industrial buyer onboarding (pulp/puree factories, sauce makers, FPOs).
- Net realization calculator (Offered Price - Transport - Handling).
- Quotation review and order voucher tracking.

## Phase 5: Field Pilot & Validation
- Pilot with 500+ farmers across Dindigul and Coimbatore tomato clusters in Tamil Nadu.
- Collaboration with local FPO and KVK (Krishi Vigyan Kendra) extension officers.
- Key Success Metrics:
  - Average farmer revenue recovery on distressed crops (Target: >₹15,000/acre recovered).
  - PMFBY claim submission within 72h window (Target: >95% on-time reporting).
  - Crop recommendation adoption rate and net profit satisfaction.
