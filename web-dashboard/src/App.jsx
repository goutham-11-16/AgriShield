import React, { useState } from 'react';

const mockReports = [
  {
    id: "DR-7A8B12CD",
    farmer: "K. Murugan",
    village: "Oddanchatram, Dindigul",
    crop: "Tomato (தக்காளி)",
    incidentDate: "2026-11-06",
    hoursRemaining: 48.0,
    area: "2.5 Acres",
    damage: "70%",
    status: "URGENT_WITHIN_72H",
    sdrfEstimated: "₹17,200",
    lossCause: "Cyclone Inundation (கனமழை வெள்ளம்)"
  },
  {
    id: "DR-9F22E401",
    farmer: "S. Selvaraj",
    village: "Reddiarchatram, Dindigul",
    crop: "Chillies (மிளகாய்)",
    incidentDate: "2026-11-05",
    hoursRemaining: 24.0,
    area: "1.8 Acres",
    damage: "55%",
    status: "CRITICAL_ACTION_REQUIRED",
    sdrfEstimated: "₹12,384",
    lossCause: "Heavy Downpour & Fruit Rot"
  }
];

const mockSalvageListings = [
  {
    id: "LIST-9812A",
    farmer: "P. Muthusamy",
    crop: "Tomato",
    qty: "4,200 kg",
    grade: "Grade B (Industrial Processing)",
    bestBuyer: "Nilakottai Puree Processing Ltd",
    offeredPrice: "₹11.50/kg",
    transportDeduction: "₹1.20/kg",
    netRealization: "₹10.30/kg",
    totalNetPayout: "₹43,260",
    safetyStatus: "VERIFIED SAFE FOR PROCESSING"
  }
];

export default function App() {
  const [activeTab, setActiveTab] = useState('recover');
  const [reports, setReports] = useState(mockReports);

  const handleEndorse = (id) => {
    alert(`Claim Dossier ${id} officially endorsed. Sent to District Agricultural Office & PMFBY Portal.`);
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Top Navbar */}
      <header style={{ background: '#1b5e20', color: '#fff', padding: '16px 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '24px' }}>🛡️</span>
            <h1 style={{ fontSize: '20px', fontWeight: '700', letterSpacing: '-0.5px' }}>AgriShield Officer &amp; FPO Portal</h1>
          </div>
          <p style={{ fontSize: '13px', color: '#a5d6a7', marginTop: '2px' }}>Pilot Region: Tamil Nadu (Dindigul &amp; Coimbatore Clusters) • Predict, Protect &amp; Recover</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <span style={{ background: '#2e7d32', padding: '6px 12px', borderRadius: '16px', fontSize: '13px', fontWeight: '600' }}>
            🟢 Sync Protocol: Active (Port 8000)
          </span>
          <span style={{ fontSize: '14px', opacity: 0.9 }}>Officer ID: TN-AGRI-4091</span>
        </div>
      </header>

      {/* Main Content Area */}
      <main style={{ maxWidth: '1200px', margin: '24px auto', padding: '0 16px', width: '100%', flex: 1 }}>
        {/* KPI Summary Cards */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '24px' }}>
          <div style={{ background: '#fff', padding: '18px', borderRadius: '10px', border: '1px solid #e2e8f0', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
            <div style={{ fontSize: '13px', color: '#718096', fontWeight: '600' }}>Registered Farmers</div>
            <div style={{ fontSize: '24px', fontWeight: '700', color: '#1b5e20', marginTop: '4px' }}>1,248</div>
            <div style={{ fontSize: '12px', color: '#48bb78', marginTop: '4px' }}>↑ 18 this week</div>
          </div>
          <div style={{ background: '#fff', padding: '18px', borderRadius: '10px', border: '1px solid #e2e8f0', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
            <div style={{ fontSize: '13px', color: '#718096', fontWeight: '600' }}>Monitored Farmland</div>
            <div style={{ fontSize: '24px', fontWeight: '700', color: '#2d3748', marginTop: '4px' }}>3,150 Acres</div>
            <div style={{ fontSize: '12px', color: '#718096', marginTop: '4px' }}>78% Drip / Precision</div>
          </div>
          <div style={{ background: '#fff', padding: '18px', borderRadius: '10px', border: '1px solid #fed7d7', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
            <div style={{ fontSize: '13px', color: '#c53030', fontWeight: '600' }}>PMFBY 72h Pending Claims</div>
            <div style={{ fontSize: '24px', fontWeight: '700', color: '#e53e3e', marginTop: '4px' }}>{reports.length} Active</div>
            <div style={{ fontSize: '12px', color: '#e53e3e', marginTop: '4px' }}>⚠️ 2 expiring within 48h</div>
          </div>
          <div style={{ background: '#fff', padding: '18px', borderRadius: '10px', border: '1px solid #e2e8f0', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
            <div style={{ fontSize: '13px', color: '#718096', fontWeight: '600' }}>Distressed Produce Salvaged</div>
            <div style={{ fontSize: '24px', fontWeight: '700', color: '#2b6cb0', marginTop: '4px' }}>18.5 Tons</div>
            <div style={{ fontSize: '12px', color: '#3182ce', marginTop: '4px' }}>₹1,94,000 recovered</div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div style={{ display: 'flex', gap: '8px', borderBottom: '2px solid #e2e8f0', marginBottom: '20px' }}>
          {[
            { id: 'recover', label: '⏱️ Post-Disaster Claims & PMFBY 72h Monitor' },
            { id: 'reconnect', label: '🏭 Distressed Produce & Buyer Matching' },
            { id: 'protect', label: '🛡️ Agro-Weather & Blight Alerts' },
            { id: 'predict', label: '🌱 Forward Price & Crop Models' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                padding: '12px 18px',
                border: 'none',
                background: 'none',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: activeTab === tab.id ? '700' : '500',
                color: activeTab === tab.id ? '#1b5e20' : '#4a5568',
                borderBottom: activeTab === tab.id ? '3px solid #1b5e20' : '3px solid transparent',
                marginBottom: '-2px'
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab 1: Recover - PMFBY 72-Hour Monitor */}
        {activeTab === 'recover' && (
          <div style={{ background: '#fff', borderRadius: '10px', padding: '24px', border: '1px solid #e2e8f0' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <div>
                <h2 style={{ fontSize: '18px', fontWeight: '700', color: '#1a202c' }}>Post-Disaster Crop Loss Reports (PMFBY 72-Hour Calamity Window)</h2>
                <p style={{ fontSize: '13px', color: '#718096' }}>Localized calamities must be intimated within 72 hours under PMFBY guidelines to guarantee surveyor empanelment.</p>
              </div>
              <button 
                onClick={() => alert("Downloading combined PMFBY district dossier...")}
                style={{ background: '#1b5e20', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: '6px', fontWeight: '600', cursor: 'pointer', fontSize: '13px' }}
              >
                📄 Export Batch PMFBY Dossier
              </button>
            </div>

            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '14px' }}>
                <thead>
                  <tr style={{ background: '#f7fafc', borderBottom: '2px solid #e2e8f0' }}>
                    <th style={{ padding: '12px' }}>Dossier ID</th>
                    <th style={{ padding: '12px' }}>Farmer &amp; Location</th>
                    <th style={{ padding: '12px' }}>Crop &amp; Loss Cause</th>
                    <th style={{ padding: '12px' }}>Affected Area &amp; Loss</th>
                    <th style={{ padding: '12px' }}>PMFBY 72h Deadline</th>
                    <th style={{ padding: '12px' }}>SDRF Input Relief</th>
                    <th style={{ padding: '12px' }}>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {reports.map((r) => (
                    <tr key={r.id} style={{ borderBottom: '1px solid #edf2f7' }}>
                      <td style={{ padding: '12px', fontWeight: '600', color: '#2b6cb0' }}>{r.id}</td>
                      <td style={{ padding: '12px' }}>
                        <div style={{ fontWeight: '600' }}>{r.farmer}</div>
                        <div style={{ fontSize: '12px', color: '#718096' }}>{r.village}</div>
                      </td>
                      <td style={{ padding: '12px' }}>
                        <div>{r.crop}</div>
                        <div style={{ fontSize: '12px', color: '#e53e3e' }}>{r.lossCause}</div>
                      </td>
                      <td style={{ padding: '12px' }}>
                        <div>{r.area}</div>
                        <div style={{ fontSize: '12px', fontWeight: '600', color: '#c53030' }}>{r.damage} Damage</div>
                      </td>
                      <td style={{ padding: '12px' }}>
                        <span style={{ background: '#fed7d7', color: '#c53030', padding: '4px 8px', borderRadius: '12px', fontSize: '12px', fontWeight: '700' }}>
                          ⏱️ {r.hoursRemaining} Hours Left
                        </span>
                      </td>
                      <td style={{ padding: '12px', fontWeight: '700', color: '#2e7d32' }}>{r.sdrfEstimated}</td>
                      <td style={{ padding: '12px' }}>
                        <button
                          onClick={() => handleEndorse(r.id)}
                          style={{ background: '#2e7d32', color: '#fff', border: 'none', padding: '6px 12px', borderRadius: '4px', cursor: 'pointer', fontSize: '12px', fontWeight: '600' }}
                        >
                          Endorse Claim
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Tab 2: Reconnect - Distressed Produce Marketplace */}
        {activeTab === 'reconnect' && (
          <div style={{ background: '#fff', borderRadius: '10px', padding: '24px', border: '1px solid #e2e8f0' }}>
            <h2 style={{ fontSize: '18px', fontWeight: '700', marginBottom: '6px' }}>Distressed &amp; Industrial-Grade Produce Liquidation</h2>
            <p style={{ fontSize: '13px', color: '#718096', marginBottom: '16px' }}>
              Connect farmers with verified food processing buyers (pulp, puree, sauce) for rain-blemished produce. Strictly rejected if mouldy or rotten.
            </p>

            {mockSalvageListings.map(item => (
              <div key={item.id} style={{ border: '1px solid #e2e8f0', borderRadius: '8px', padding: '16px', marginBottom: '12px', background: '#fafafa' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div>
                    <span style={{ background: '#e2e8f0', padding: '2px 8px', borderRadius: '4px', fontSize: '11px', fontWeight: '600' }}>{item.id}</span>
                    <h3 style={{ fontSize: '16px', fontWeight: '700', marginTop: '4px' }}>{item.farmer} • {item.crop} ({item.qty})</h3>
                    <div style={{ fontSize: '13px', color: '#4a5568', marginTop: '2px' }}>Quality: <b>{item.grade}</b></div>
                    <div style={{ fontSize: '12px', color: '#2e7d32', fontWeight: '600', marginTop: '2px' }}>✓ {item.safetyStatus}</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '12px', color: '#718096' }}>Matched Industrial Buyer</div>
                    <div style={{ fontSize: '14px', fontWeight: '700', color: '#1b5e20' }}>{item.bestBuyer}</div>
                    <div style={{ fontSize: '13px', color: '#4a5568', marginTop: '4px' }}>Offered: {item.offeredPrice} • Transport: {item.transportDeduction}</div>
                    <div style={{ fontSize: '15px', fontWeight: '700', color: '#2b6cb0', marginTop: '2px' }}>
                      Net Realization: {item.netRealization} (Payout: {item.totalNetPayout})
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Tab 3: Protect - Weather & Blight Advisories */}
        {activeTab === 'protect' && (
          <div style={{ background: '#fff', borderRadius: '10px', padding: '24px', border: '1px solid #e2e8f0' }}>
            <h2 style={{ fontSize: '18px', fontWeight: '700', marginBottom: '6px' }}>Agro-Meteorological Risk Monitoring</h2>
            <p style={{ fontSize: '13px', color: '#718096', marginBottom: '16px' }}>7-Day rolling forecast from Open-Meteo &amp; IMD Agromet Bulletins for Dindigul cluster.</p>
            <div style={{ background: '#fffaf0', border: '1px solid #feebc8', borderRadius: '8px', padding: '16px', marginBottom: '16px' }}>
              <div style={{ fontWeight: '700', color: '#c05621' }}>⚠️ High Humidity Alert: Early/Late Blight in Solanaceous Crops</div>
              <p style={{ fontSize: '13px', color: '#7b341e', marginTop: '4px' }}>
                Relative humidity &gt;75% with moderate temperatures creates fungal spore conditions.
                Broadcasted advisory to 450 tomato farmers in Oddanchatram block: Apply protective bio-fungicide (Pseudomonas fluorescens 0.2%).
              </p>
            </div>
          </div>
        )}

        {/* Tab 4: Predict - Forward Crop Price Models */}
        {activeTab === 'predict' && (
          <div style={{ background: '#fff', borderRadius: '10px', padding: '24px', border: '1px solid #e2e8f0' }}>
            <h2 style={{ fontSize: '18px', fontWeight: '700', marginBottom: '6px' }}>Pre-Cultivation Decision Engine &amp; Harvest Price Forecasts</h2>
            <p style={{ fontSize: '13px', color: '#718096', marginBottom: '16px' }}>Forward price estimations at expected harvest windows based on 5-year AGMARKNET seasonal indices.</p>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
              <div style={{ border: '1px solid #e2e8f0', borderRadius: '8px', padding: '16px' }}>
                <h3 style={{ fontSize: '16px', fontWeight: '700' }}>தக்காளி (Tomato)</h3>
                <div style={{ fontSize: '13px', color: '#718096' }}>Duration: 105 Days • Water: 500mm</div>
                <div style={{ marginTop: '12px', fontSize: '13px' }}>
                  <div>Pessimistic: <b style={{ color: '#e53e3e' }}>₹8.0/kg</b></div>
                  <div>Normal: <b style={{ color: '#2e7d32' }}>₹16.0/kg</b></div>
                  <div>Optimistic: <b style={{ color: '#2b6cb0' }}>₹26.0/kg</b></div>
                </div>
              </div>
              <div style={{ border: '1px solid #e2e8f0', borderRadius: '8px', padding: '16px' }}>
                <h3 style={{ fontSize: '16px', fontWeight: '700' }}>நிலக்கடலை (Groundnut)</h3>
                <div style={{ fontSize: '13px', color: '#718096' }}>Duration: 115 Days • Water: 450mm</div>
                <div style={{ marginTop: '12px', fontSize: '13px' }}>
                  <div>Pessimistic: <b style={{ color: '#e53e3e' }}>₹58.0/kg</b></div>
                  <div>Normal: <b style={{ color: '#2e7d32' }}>₹68.0/kg</b></div>
                  <div>Optimistic: <b style={{ color: '#2b6cb0' }}>₹80.0/kg</b></div>
                </div>
              </div>
              <div style={{ border: '1px solid #e2e8f0', borderRadius: '8px', padding: '16px' }}>
                <h3 style={{ fontSize: '16px', fontWeight: '700' }}>மக்காச்சோளம் (Maize)</h3>
                <div style={{ fontSize: '13px', color: '#718096' }}>Duration: 100 Days • Water: 400mm</div>
                <div style={{ marginTop: '12px', fontSize: '13px' }}>
                  <div>Pessimistic: <b style={{ color: '#e53e3e' }}>₹19.5/kg</b></div>
                  <div>Normal: <b style={{ color: '#2e7d32' }}>₹23.5/kg</b></div>
                  <div>Optimistic: <b style={{ color: '#2b6cb0' }}>₹27.0/kg</b></div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer style={{ background: '#fff', borderTop: '1px solid #e2e8f0', padding: '16px', textAlign: 'center', fontSize: '13px', color: '#718096' }}>
        AgriShield Agricultural Decision &amp; Disaster Recovery Platform • Designed for Indian Agriculture • Pilot: Tamil Nadu
      </footer>
    </div>
  );
}
