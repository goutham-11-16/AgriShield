# AgriShield – Predict, Protect & Recover

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.14-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-teal.svg)](https://fastapi.tiangolo.com/)
[![Android](https://img.shields.io/badge/Android-Kotlin%20%7C%20Compose-purple.svg)](https://developer.android.com/)
[![Target](https://img.shields.io/badge/Target_Pilot-Tamil_Nadu%2C_India-orange.svg)]()

> **AgriShield** is a practical, scalable, offline-first agricultural decision-support and disaster-recovery platform engineered for Indian farmers. It bridges pre-cultivation planning, localized early-warning risk management, post-disaster insurance claim assistance, and alternative salvage market recovery.

---

## 🌟 The Four Core Modules

```
                    ┌──────────────────────────────────────────────┐
                    │                  AgriShield                  │
                    │         Predict, Protect & Recover           │
                    └──────────────────────┬───────────────────────┘
                                           │
         ┌──────────────────┬──────────────┴─────┬──────────────────┐
         ▼                  ▼                    ▼                  ▼
   ┌───────────┐      ┌───────────┐        ┌───────────┐      ┌───────────┐
   │ MODULE A  │      │ MODULE B  │        │ MODULE C  │      │ MODULE D  │
   │  PREDICT  │      │  PROTECT  │        │  RECOVER  │      │ RECONNECT │
   └─────┬─────┘      └─────┬─────┘        └─────┬─────┘      └─────┬─────┘
         │                  │                    │                  │
   • Soil & Region    • 7-Day Agro-        • Disaster loss    • Grade B/C
     Suitability        Weather Alerts       evidence & photo   produce salvage
   • Forward Harvest  • Heavy Rain &         capture          • Verified puree/
     Price Scenarios    Cyclone Warnings   • 72h PMFBY          pulp/sauce
   • 3-Crop Profit    • Stage-Specific       timer countdown    buyers
     Comparison         Advisories         • Official claim   • Net realization
   • Risk & Subsidies • Fungal / Blight      dossier PDF        calculator
                        risk index         • SDRF/NDRF info
```

1. **Module A – PREDICT (Pre-Cultivation Decision Engine):** Answers *"Which crop should I grow to maximize profitability?"* using multi-criteria suitability and **forward harvest price distributions** (Optimistic, Normal, Pessimistic) rather than misleading spot rates.
2. **Module B – PREPARE & PROTECT (Cultivation Monitoring):** Answers *"What risks are approaching and what actions should I take?"* with real-time agro-meteorological monitoring, localized warnings (heavy rain, cyclone, heat stress, fungal blights), and phenological stage advisories in Tamil and English.
3. **Module C – RECOVER (Disaster Management & Insurance):** Answers *"How do I report losses, protect remaining crops, and apply for relief?"* with geotagged evidence capture, automated countdown against the **PMFBY 72-hour localized calamity rule**, generated claim dossiers, and direct connection to KVK/FPO officers.
4. **Module D – RECONNECT (Salvage & Alternative Buyer Discovery):** Answers *"Where can I sell damaged or surplus produce?"* by connecting farmers with industrial food processing buyers (tomato puree, pulp, paste, sauce, cattle feed) with transparent net-realization logistics calculation.

---

## 📊 Agricultural Data Source Audit Summary

| Source | Provider | API Status | Cost / Tier | Purpose in AgriShield |
|---|---|---|---|---|
| **Mandi Rates & Arrivals** | data.gov.in / AGMARKNET | Public REST JSON | Free (Registration) | Historical & current mandi prices |
| **Agro-Weather Forecast** | Open-Meteo | Public REST JSON | Free (<10k/day) | Hourly precipitation, soil moisture, ET0 |
| **Solar & Historical Climate**| NASA POWER | Public REST JSON | Free Open Public | Thermal units (GDD) & historical rain |
| **Cyclone & Weather Alerts** | IMD Mausam | Public CAP RSS / XML | Free Public | National severe weather alert polygons |
| **Crop Practices & Calendars**| TNAU / ICAR | Curated Agronomic | Open Extension | Tamil Nadu crop stages & input costs |
| **Crop Insurance** | PMFBY Portal | Official Assisted | Govt Portal | 72h rule workflow & loss claim dossiers |
| **Soil Macro/Micro Nutrients**| Soil Health Card | Curated District Baseline| Public Records | District nutrient benchmarking |

---

## 📂 Repository Directory Layout

```text
AgriShield/
│
├── android-app/          # Offline-first Android application (Kotlin, Jetpack Compose, Room DB)
├── backend/              # Python FastAPI backend (Services, Models, API endpoints, Sync)
├── web-dashboard/        # FPO, KVK & Officer web dashboard (React, Vite, Tailwind CSS)
├── ml-engine/            # Crop suitability, price forecasting, and risk prediction algorithms
├── database/             # PostgreSQL + PostGIS schemas, SQLite fallback, seed migrations
├── data-pipelines/       # Open-Meteo, data.gov.in Mandi price, and TNAU data fetchers
├── documentation/        # Full technical specifications and official API guides
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── API_AND_DATA_SOURCE_GUIDE.md
│   ├── API_SETUP.md
│   ├── DATABASE_SCHEMA.md
│   ├── AI_ML_DESIGN.md
│   ├── OFFLINE_FIRST_DESIGN.md
│   ├── SECURITY_AND_PRIVACY.md
│   ├── COMPETITOR_ANALYSIS.md
│   ├── MVP_ROADMAP.md
│   └── DEPLOYMENT_GUIDE.md
│
├── scripts/              # Seed scripts, data loaders, demo runners
├── tests/                # Automated unit and integration test suite
├── .env.example          # Environment variable template
├── .gitignore            # Git exclusion rules
├── README.md             # Project documentation
└── LICENSE               # Apache 2.0 Open Source License
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.11+
- Node.js 18+
- Android Studio (for mobile development)

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and supply your DATA_GOV_IN_API_KEY (optional for local demo seed data)
```

### 3. Backend Setup & Startup
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m app.db.init_db
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
View interactive Swagger API docs at `http://localhost:8000/docs`.

### 4. Web Dashboard Setup
```bash
cd web-dashboard
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 🛡️ License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
