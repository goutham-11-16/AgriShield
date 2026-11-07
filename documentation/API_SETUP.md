# AgriShield - API Setup & Credential Management Guide

This document explains step-by-step how to configure all credentials required to run AgriShield in local development, staging, and production environments.

> **Security Rule:** Never commit API keys or secret files to Git. All secrets must be provided via `.env` or system environment variables. The Android client communicates strictly with the AgriShield Backend proxy and never stores external vendor keys.

---

## 1. Quick Start (.env Configuration)

1. In the project root, copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and configure the variables described below.

---

## 2. API Credentials Breakdown

### A. Open Government Data Platform (data.gov.in)

- **Provider Name:** National Informatics Centre (NIC), Government of India
- **Official URL:** `https://data.gov.in/`
- **Purpose:** Daily Mandi prices and commodity arrivals across Indian APMC markets.
- **Registration Steps:**
  1. Visit `https://data.gov.in/user/register`.
  2. Enter your Name, Email, Indian Mobile Number, and select user type (e.g. "Individual/Developer").
  3. Validate using the SMS OTP sent to your phone and the activation link in your email.
- **Where to Find the API Key:**
  1. Log in at `https://data.gov.in/user/login`.
  2. In the top navigation, click on **"My Account"** -> **"API Key Management"**.
  3. Copy your 64-character alphanumeric API Key.
- **Billing Required:** No. 100% Free public service.
- **Free Usage Limits:** 10,000 requests per day; max 1,000 records per call.
- **How to Test the Credential:**
  ```bash
  curl -X GET "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=YOUR_API_KEY&format=json&limit=2"
  ```
- **Configuration in Project:**
  Set `DATA_GOV_IN_API_KEY` in `.env`:
  ```env
  DATA_GOV_IN_API_KEY=your_key_here
  ```

---

### B. Open-Meteo Agro-Weather API

- **Provider Name:** Open-Meteo GmbH
- **Official URL:** `https://open-meteo.com/`
- **Purpose:** 7-day hourly weather forecasts, rainfall, soil moisture (0-7cm), soil temperature, and ET0.
- **Registration Steps:**
  - **Free Tier:** No registration or API key is required.
  - **Commercial Tier:** If deployed commercially exceeding 10,000 calls/day, register at `https://open-meteo.com/en/pricing`.
- **Where to Find the API Key:** Provided in customer portal after commercial plan activation.
- **Billing Required:** None for development, non-commercial, and light production (< 10,000 calls/day).
- **Free Usage Limits:** Up to 10,000 requests per day, max 60 calls per minute.
- **How to Test:**
  ```bash
  curl -s "https://api.open-meteo.com/v1/forecast?latitude=11.1271&longitude=78.6569&current=temperature_2m,precipitation"
  ```
- **Configuration in Project:**
  Set `OPEN_METEO_API_KEY` in `.env` (leave empty for standard free tier):
  ```env
  OPEN_METEO_API_KEY=
  ```

---

### C. NASA POWER API (Agricultural Climatology)

- **Provider Name:** NASA Earth Science Division / Langley Research Center
- **Official URL:** `https://power.larc.nasa.gov/`
- **Purpose:** Solar radiation (ALLSKY_SFC_SW_DWN), Growing Degree Days (GDD), and historical precipitation.
- **Registration Steps:** None. Open access.
- **API Key Required:** No.
- **Billing Required:** Free of charge.
- **How to Test:**
  ```bash
  curl -s "https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,PRECTOTCORR&community=AG&longitude=78.65&latitude=11.12&start=20240101&end=20240103&format=JSON"
  ```
- **Configuration in Project:** No configuration variable required; built into data pipeline client.

---

### D. Digital India Bhashini (Voice & Indic Translation) - Optional

- **Provider Name:** National Language Translation Mission (NLTM), MeitY, Govt of India
- **Official URL:** `https://bhashini.gov.in/`
- **Purpose:** High-accuracy Speech-to-Text (ASR) and Text-to-Speech (TTS) for Tamil, Telugu, Hindi, Kannada, Malayalam.
- **Registration Steps:**
  1. Visit `https://bhashini.gov.in/en/join-ecosystem`.
  2. Register your organization/developer profile on the ULCA platform.
  3. Submit an application detailing your agricultural public-good application.
- **Where to Find the API Key:** ULCA Dashboard -> API Credentials.
- **Billing Required:** Free for approved public interest and research projects.
- **Offline Fallback:** AgriShield Android app automatically falls back to native `android.speech` if Bhashini is unreachable or offline.
- **Configuration in Project:**
  ```env
  BHASHINI_USER_ID=your_user_id
  BHASHINI_API_KEY=your_bhashini_key
  BHASHINI_PIPELINE_ID=your_pipeline_id
  ```

---

### E. Backend Security Secret Key

- **Purpose:** Cryptographic signing of JWT authentication tokens for Farmers, FPOs, and Admin Officers.
- **Generation Method:** Run the following command in terminal:
  ```bash
  python3 -c "import secrets; print(secrets.token_hex(32))"
  ```
- **Configuration in Project:**
  ```env
  SECRET_KEY=paste_the_64_char_hex_here
  ```

---

## 3. Secret Management & Production Hardening

1. **Proxy Architecture:**
   The Android application **never** talks directly to external paid or authenticated APIs. The Android client only connects to:
   `https://api.yourdomain.org/api/v1/...`
   The backend injects all upstream credentials securely on the server.
2. **Environment Isolation:**
   Use separate keys for staging and production.
3. **Audit & Rotation:**
   Rotate `SECRET_KEY` and third-party tokens every 90 days.
