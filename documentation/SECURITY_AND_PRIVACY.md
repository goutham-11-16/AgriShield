# AgriShield - Security, Privacy & Compliance Architecture

## 1. Compliance with Digital Personal Data Protection (DPDP) Act, 2023

AgriShield is designed to uphold the highest standards of data fiduciary responsibility towards Indian agricultural communities:

1. **Lawful Purpose & Explicit Consent:**
   - GPS coordinates and farm boundaries are requested strictly for localized agro-weather advisories and disaster claim verification.
   - Clear multi-lingual consent prompts (Tamil & English) explain why location and camera access are needed.
2. **Right to Withdraw & Erasure:**
   - Farmers can request complete deletion of their profile and farm records directly from app settings or via their FPO coordinator.
3. **Strict Non-Commercialization:**
   - **AgriShield never sells, leases, or trades farmer personal data, land records, or yield details to third-party marketing brokers.**

---

## 2. Role-Based Access Control (RBAC)

AgriShield enforces strict role segregation via JWT claims:

| Role | Permissions |
|---|---|
| **Farmer** | Read own farm data, run crop predictions, view weather/mandi rates, submit disaster claims, list produce for sale, view quotations. |
| **FPO / Officer** | View registered farmers in assigned block/district, verify disaster claims, assist offline synchronization, endorse produce listings. |
| **Buyer** | View anonymized produce listings (quantity, district, grade), submit binding price quotations, arrange logistics. **Cannot see farmer personal phone number until quotation is accepted.** |
| **Platform Admin** | Manage master agronomic catalogs, verify buyer GSTIN/FSSAI credentials, monitor system health. |

---

## 3. Buyer Verification & Fraud Prevention

To prevent predatory middlemen or fraudulent industrial buyer accounts:
1. **Statutory Document Verification:**
   - Mandatory Goods and Services Tax Identification Number (**GSTIN**).
   - Food Safety and Standards Authority of India (**FSSAI**) manufacturing license for food processors.
2. **Escrow & Quotation Integrity:**
   - Buyer quotations submitted on the platform are legally binding for the stated validity window (e.g., 48 hours).
   - Once a quotation is accepted by a farmer, a formal procurement voucher is generated with transparent deduction clauses (handling/transport).

---

## 4. API & Credential Security

- **Zero Client-Side Secrets:** Android APKs and web bundles contain zero external API keys.
- **Backend API Gateway Proxy:** All upstream queries (data.gov.in, Open-Meteo, Bhashini) are brokered by the FastAPI backend.
- **Transport Security:** All client-server communications are enforced via TLS 1.3 with HTTP Strict Transport Security (HSTS).
