# AgriShield - AI & ML Engine Design

## 1. Principles of AgriShield AI/ML

1. **Deterministic Agronomy First:** Core crop suitability, water requirements, and crop duration rules are grounded in established scientific recommendations from ICAR (Indian Council of Agricultural Research) and TNAU (Tamil Nadu Agricultural University).
2. **Never Present Predictions as Certainties:** Forward market prices are forecast with confidence bounds and explicitly presented as three scenarios: **Optimistic**, **Normal**, and **Pessimistic**.
3. **Food Safety Integrity:** Computer vision or heuristics are used to categorize produce grade, but **strictly never** certify chemical or microbiological safety. Any mouldy, foul-smelling, or rotten produce is hard-coded as **UNSAFE** for human food or animal feed.
4. **Full Provenance & Explainability:** Every recommendation outputs the underlying features (e.g. soil pH compatibility, rainfall window, historical mandi price delta) and data source timestamps.

---

## 2. Model 1: Pre-Cultivation Crop Suitability & 3-Crop Comparator

### Input Feature Vector
$$X = [\text{District}, \text{SoilType}, \text{Soil\_pH}, \text{IrrigationType}, \text{WaterAvailability\_Score}, \text{SowingMonth}, \text{BudgetPerAcre}]$$

### Agronomic Suitability Score ($S_c \in [0, 100]$)
For each candidate crop $c$:
$$S_c = w_{\text{soil}} \cdot S_{\text{soil}}(c) + w_{\text{water}} \cdot S_{\text{water}}(c) + w_{\text{season}} \cdot S_{\text{season}}(c) + w_{\text{budget}} \cdot S_{\text{budget}}(c)$$
where weights satisfy $\sum w_i = 1.0$ ($w_{\text{soil}}=0.30, w_{\text{water}}=0.35, w_{\text{season}}=0.20, w_{\text{budget}}=0.15$).

### Expected Harvest Date
$$\text{HarvestDate} = \text{SowingDate} + \text{GrowthDurationDays}(c)$$

---

## 3. Model 2: Forward Harvest Price Forecasting (Seasonal Mandi Engine)

Instead of naive spot prices, AgriShield predicts the expected wholesale price in the **harvest month window** ($\pm 15$ days of predicted harvest date).

### Historical Time-Series Decomposition
For monthly mandi modal prices $P_t$:
$$P_t = T_t + S_t + \epsilon_t$$
where $T_t$ is long-term trend, $S_t$ is the monthly seasonal index for Tamil Nadu APMC mandis, and $\epsilon_t$ is stochastic variance.

### 3-Tier Price Scenario Estimation
Given base forecast $\hat{P}$:
- **Normal Scenario ($P_{50}$):** Median expected price based on seasonal index.
- **Optimistic Scenario ($P_{75}$):** $P_{50} \times (1 + \sigma_{\text{historical}} \cdot 1.15)$ (Favorable demand, reduced regional glut).
- **Pessimistic Scenario ($P_{25}$):** $P_{50} \times (1 - \sigma_{\text{historical}} \cdot 1.15)$ (Market glut, sudden arrival surges).

### Economic Realization
$$\text{Revenue}_{\text{scenario}} = \text{YieldPerAcre} \times \text{Acres} \times P_{\text{scenario}}$$
$$\text{NetProfit}_{\text{scenario}} = \text{Revenue}_{\text{scenario}} - (\text{CultivationCostPerAcre} \times \text{Acres})$$

---

## 4. Model 3: Agro-Meteorological Early Warning Rules

AgriShield monitors Open-Meteo forecasts against phenological stages (Vegetative, Flowering, Fruiting, Mature):

| Parameter | Threshold | Vulnerable Crop / Stage | Alert Level | Action Plan |
|---|---|---|---|---|
| **24h Rainfall** | $> 65 \text{ mm}$ | Tomato, Cotton (Flowering/Fruiting) | **Critical** | Trench field boundaries immediately to drain standing water; brace stakes. |
| **Wind Gusts** | $> 55 \text{ km/h}$ | Banana, Sugarcane, Tomato | **High** | Earth up soil around root zone; provide bamboo supports to prevent lodging. |
| **Max Temperature** | $> 38^\circ\text{C}$ for 3 days | Tomato, Chillies (Flowering) | **Medium** | Apply light evening irrigation or micro-sprinklers to prevent flower drop. |
| **RH & Temp Combo** | $\text{RH} > 85\% \land T \in [20, 26]^\circ\text{C}$ | Tomato, Potato | **High** | High risk of Early/Late Blight fungal spore germination. Apply protective bio-fungicide (Trichoderma viride or copper hydroxide). |

---

## 5. Model 4: Post-Disaster Produce Classification & Fair Valuation

When crops are damaged, farmers need alternative liquidation:
- **Grade B (Industrial Processing):** Fruit intact, skin blemishes or minor cracks, firmness $> 2.5 \text{ kg/cm}^2$, no decay. Suitable for tomato paste, ketchup, juice, dehydration.
- **Grade C (Livestock Feed / Compost):** Crushed or bruised, overripe, clean but non-marketable.
- **Unsafe (Biohazard):** Any fungal mycelium, bacterial soft rot, foul odor, or chemical inundation. Strictly blocked from marketplace.

### Fair Realization Formula
$$\text{Farmer Net Return (₹/kg)} = \text{Buyer Quote} - \text{Transport Cost/kg} - \text{Loading/Grading Cost/kg}$$
