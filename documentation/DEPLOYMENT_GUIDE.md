# AgriShield - Deployment & Operations Guide

## 1. System Requirements

- **Server OS:** Ubuntu 22.04 LTS / Debian 12 / Any standard Linux distribution.
- **Python:** 3.11+ (Python 3.14 compatible).
- **Node.js:** v18+ / v20+ / v22+ (for Web Dashboard).
- **Database:** PostgreSQL 15+ with PostGIS 3+ (or SQLite with SpatiaLite for local demo).
- **Memory & Storage:** 2 vCPU, 4GB RAM minimum (scales horizontally).

---

## 2. Local Development Setup

### A. Backend Setup
1. Clone the repository and navigate to backend:
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Configure `.env`:
   ```bash
   cp ../.env.example .env
   ```
3. Run database migrations or initial seed:
   ```bash
   python3 -m app.db.init_db
   ```
4. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   API interactive docs will be available at: `http://localhost:8000/docs`

### B. Web Dashboard Setup
1. Navigate to `web-dashboard`:
   ```bash
   cd ../web-dashboard
   npm install
   npm run dev
   ```
2. Access the dashboard at `http://localhost:5173`.

### C. Android App
1. Open the `android-app` directory in Android Studio (Koala / Ladybug or newer).
2. Sync Gradle files.
3. Update `BASE_URL` in `BuildConfig` or `AppConfig.kt` to your backend URL (`http://10.0.2.2:8000` for Android emulator, or your LAN IP).
4. Build and run on emulator or connected device.

---

## 3. Production Deployment with Docker Compose

A production-grade `docker-compose.yml` provides:
- FastAPI backend on ASGI workers (Uvicorn / Gunicorn).
- PostgreSQL 16 with PostGIS extension.
- Nginx reverse proxy with SSL termination and rate limiting.
- Automatic daily data sync worker for AGMARKNET Mandi prices.

```bash
docker compose up -d --build
```
