# AgriShield: Predict, Protect and Recover

AgriShield is an agricultural decision-support and recovery platform designed for Indian farmers, field coordinators, Farmer Producer Organizations (FPOs), and agricultural officers. It bridges pre-cultivation crop selection, real-time localized weather risk monitoring, post-disaster insurance claim assistance, and distressed produce market salvage.

The initial pilot implementation focuses on Tamil Nadu (specifically the Dindigul and Coimbatore horticulture clusters), with architecture designed to scale across all Indian agro-climatic zones.

---

## The Four Core Modules

### 1. Module A: Predict (Pre-Cultivation Decision Engine)
- Solves the problem of volatile spot market prices by estimating forward wholesale price distributions around projected harvest dates rather than using today's mandi price.
- Multi-criteria agronomic suitability scoring based on soil type, soil pH, irrigation source, crop duration, and cultivation budget.
- Side-by-side comparison of three candidate crops.
- Forward price distributions presented in three explicit scenarios:
  - Pessimistic Scenario (Low demand / regional harvest glut)
  - Normal Scenario (Expected 50th percentile historical price)
  - Optimistic Scenario (High demand / supply shortfall)
- Calculates expected yield, cultivation expenses, gross revenue, net profit, and return on investment (ROI).
- Incorporates applicable central and state subsidies (e.g., MIDH drip subsidy, NMEO-OS, PMFBY horticulture coverage).

### 2. Module B: Prepare and Protect (During Cultivation Monitoring)
- Real-time 7-day agro-weather monitoring using Open-Meteo forecasts calibrated with IMD agromet parameters.
- Automatic risk threshold detection:
  - Heavy rainfall (>45 mm/24h) and cyclone wind warnings
  - Heat stress (>38 deg C for 3 consecutive days during flowering)
  - Fungal blight index (humidity >75% with moderate temperatures)
- Crop-stage-specific advisories (Vegetative, Flowering, Fruiting, Maturity) with preventive cultural practices.
- Multi-lingual guidance in English and Tamil (Thamizh).

### 3. Module C: Recover (Disaster Management and PMFBY Assistance)
- Incident reporting with geotagged photo capture and crop damage quantification.
- PMFBY 72-Hour Calamity Rule Countdown: Operational guidelines mandate that localized calamities (cyclone, inundation, hailstorm, landslide) must be reported within 72 hours. The system tracks hours elapsed, calculates remaining time, and sets urgency flags.
- Tamil Nadu State Disaster Response Fund (SDRF) input subsidy relief estimator (e.g., Rs. 17,000 per hectare for irrigated crops with >33% loss).
- Generates official PMFBY Loss Notification Claim Dossiers for submission to PACCS, banks, or Common Service Centres (CSCs).
- Direct helpline access to the national toll-free crop insurance line (14447 / 1800-180-1551).

### 4. Module D: Reconnect (Alternative Market Discovery and Salvage)
- Solves the issue of post-disaster produce disposal where rain-blemished or cracked crops are rejected by retail mandis but remain sound for processing.
- Strictly separates produce grades:
  - Grade A: Retail Prime
  - Grade B: Industrial Processing (tomato paste, puree, sauce, juice, dehydration)
  - Grade C: Livestock Feed and Compost
  - Biohazard / Unsafe: Rotten or fungal-decayed produce is strictly rejected from all human or animal channels.
- Verified industrial buyer directory (food processing plants, puree manufacturers, feed compounders in Tamil Nadu food parks).
- Net Realization Calculator:
  Net Realization per kg = Offered Price - Transport Cost - Handling Cost
  Total Payout = Quantity x Net Realization

---

## Data Sources and API Audit Matrix

| Requirement | Provider | API Status | Cost / Tier | Integration Approach |
|---|---|---|---|---|
| Daily Mandi Prices | data.gov.in / AGMARKNET | REST JSON API | Free (Registration required) | Direct ingestion via OGD endpoint with local caching |
| Agro-Weather Forecast | Open-Meteo | REST JSON API | Free (<10k calls/day) | Hourly temperature, precipitation, soil moisture (0-7cm) |
| Climatology & Solar | NASA POWER | REST JSON API | Free (Public open API) | Daily solar radiation, GDD, and historical rainfall |
| Severe Weather Alerts | IMD Mausam | CAP RSS / Bulletins | Free public bulletins | Common Alerting Protocol RSS and Agromet unit parsing |
| Soil Nutrients | Soil Health Card | Curated Baselines | Public records | District NPK and micronutrient benchmarks |
| Crop Insurance | PMFBY Portal | Assisted Workflow | Govt Portal | Rule-guided 72h workflow, claim dossier generator |
| Land Use & Satellite | ISRO Bhuvan | WMS / WFS Services | Free with registration | Agro-ecological zone mapping |

---

## Architecture and Offline-First Strategy

Rural agricultural connectivity is frequently intermittent. AgriShield operates on an offline-first architecture:

1. Local Persistence: The Android client stores all farm records, cached weather, and price models locally in a SQLite database via Android Room.
2. Offline Mutations Queue: User actions (reporting crop damage, listing salvage produce) are immediately written locally and queued in an offline synchronization table.
3. WorkManager Synchronization: When internet connectivity is detected, Android WorkManager delivers queued mutations in batches to the backend endpoint (`/api/v1/sync/push`) with exponential backoff.
4. Image Compression: Geotagged damage photos are compressed to high-efficiency WebP format (<300 KB) while preserving EXIF GPS coordinates, preventing upload timeouts on 2G/3G networks.
5. Officer / FPO Mode: Field coordinators can record data on behalf of multiple farmers in disconnected villages and sync once back at an office with network access.

---

## Repository Structure

```text
AgriShield/
|-- android-app/          # Offline-first Android application (Kotlin, Jetpack Compose, Room DB)
|-- backend/              # Python FastAPI backend (Services, Models, API endpoints, Sync)
|-- web-dashboard/        # FPO, KVK and Officer web dashboard (React, Vite, Responsive UI)
|-- ml-engine/            # Crop suitability, price forecasting, and risk prediction algorithms
|-- database/             # PostgreSQL + PostGIS schemas, SQLite fallback, seed migrations
|-- data-pipelines/       # Open-Meteo, data.gov.in Mandi price, and TNAU data fetchers
|-- documentation/        # Technical specifications and official API guides
|   |-- SYSTEM_ARCHITECTURE.md
|   |-- API_AND_DATA_SOURCE_GUIDE.md
|   |-- API_SETUP.md
|   |-- DATABASE_SCHEMA.md
|   |-- AI_ML_DESIGN.md
|   |-- OFFLINE_FIRST_DESIGN.md
|   |-- SECURITY_AND_PRIVACY.md
|   |-- COMPETITOR_ANALYSIS.md
|   |-- MVP_ROADMAP.md
|   `-- DEPLOYMENT_GUIDE.md
|-- scripts/              # Seed scripts, data loaders, demo runners
|-- tests/                # Automated unit and integration test suite
|-- .env.example          # Environment variable template
|-- .gitignore            # Git exclusion rules
|-- README.md             # Project documentation
`-- LICENSE               # Apache 2.0 Open Source License
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Android Studio (for Android build)

### 1. Environment Configuration
Copy the template configuration:
```bash
cp .env.example .env
```
Configure your keys in `.env` as documented in `documentation/API_SETUP.md`.

### 2. Backend Setup
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m app.db.init_db
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive API documentation is accessible at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 3. Web Dashboard Setup
```bash
cd web-dashboard
npm install
npm run build
```
The built dashboard is automatically served by the backend at `http://localhost:8000/dashboard` or during development via:
```bash
npm run dev
```

### 4. Running Automated Tests
Run the test suite covering economic models, PMFBY 72h rule logic, food safety checks, and API endpoints:
```bash
PYTHONPATH=. backend/.venv/bin/pytest tests/ -v
```

### 5. Running the Complete Simulation
To observe an end-to-end run of all four modules (Predict, Protect, Recover, Reconnect):
```bash
backend/.venv/bin/python3 scripts/demo_simulation.py
```

---

## Security, Privacy, and Trust

- Digital Personal Data Protection (DPDP) Act 2023 compliance.
- No sale or commercial brokering of farmer data.
- Zero client-side API secrets: Android client connects solely through the backend proxy.
- Human review gate: AI models assist with initial triage but do not replace certified agricultural extension officers or statutory loss surveyors.

---

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.
