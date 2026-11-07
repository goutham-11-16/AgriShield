package org.agrishield.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// Color Palette for AgriShield
val ForestGreen = Color(0xFF1B5E20)
val SageGreen = Color(0xFF4CAF50)
val AlertRed = Color(0xFFD32F2F)
val AmberWarning = Color(0xFFFFA000)
val CardBg = Color(0xFFF9FBF9)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AgriShieldMainApp() {
    var selectedTab by remember { mutableStateOf(0) }
    var isSynced by remember { mutableStateOf(true) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text("AgriShield – அக்ரிஷீல்ட்", fontWeight = FontWeight.Bold, fontSize = 18.sp)
                        Text("Predict, Protect & Recover", fontSize = 12.sp, color = Color.White.copy(alpha = 0.8f))
                    }
                },
                actions = {
                    Surface(
                        shape = RoundedCornerShape(16.dp),
                        color = if (isSynced) Color(0xFF2E7D32) else AmberWarning,
                        modifier = Modifier.padding(end = 12.dp)
                    ) {
                        Text(
                            text = if (isSynced) "🟢 Synced" else "🟡 1 Queued",
                            color = Color.White,
                            fontSize = 12.sp,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = ForestGreen,
                    titleContentColor = Color.White
                )
            )
        },
        bottomBar = {
            NavigationBar(containerColor = Color.White) {
                NavigationBarItem(
                    selected = selectedTab == 0,
                    onClick = { selectedTab = 0 },
                    label = { Text("Predict") },
                    icon = { Text("🌱") }
                )
                NavigationBarItem(
                    selected = selectedTab == 1,
                    onClick = { selectedTab = 1 },
                    label = { Text("Protect") },
                    icon = { Text("🛡️") }
                )
                NavigationBarItem(
                    selected = selectedTab == 2,
                    onClick = { selectedTab = 2 },
                    label = { Text("Recover") },
                    icon = { Text("⏱️") }
                )
                NavigationBarItem(
                    selected = selectedTab == 3,
                    onClick = { selectedTab = 3 },
                    label = { Text("Market") },
                    icon = { Text("🏭") }
                )
            }
        }
    ) { padding ->
        Box(modifier = Modifier.padding(padding).fillMaxSize().background(Color(0xFFF4F6F4))) {
            when (selectedTab) {
                0 -> PredictScreen()
                1 -> ProtectScreen()
                2 -> RecoverScreen()
                3 -> ReconnectScreen()
            }
        }
    }
}

@Composable
fun PredictScreen() {
    LazyColumn(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        item {
            Text(
                "சாகுபடிக்கு முந்தைய பயிர் கணிப்பு (Pre-Cultivation Decision Engine)",
                fontWeight = FontWeight.Bold,
                fontSize = 16.sp,
                color = ForestGreen
            )
            Spacer(modifier = Modifier.height(12.dp))
            Card(
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp),
                elevation = CardDefaults.cardElevation(2.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Selected Plot: Dindigul • 2.0 Acres • Red Sandy Loam", fontWeight = FontWeight.SemiBold)
                    Text("Irrigation: Drip (Borewell) • Budget: ₹80,000", fontSize = 13.sp, color = Color.Gray)
                    Spacer(modifier = Modifier.height(8.dp))
                    Button(
                        onClick = { /* Run 3-crop comparison */ },
                        colors = ButtonDefaults.buttonColors(containerColor = SageGreen),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text("Top 3 Crops Comparison (3 பயிர்கள் ஒப்பீடு)")
                    }
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
            Text("Top Recommended Crops & Harvest Price Scenarios", fontWeight = FontWeight.Bold, fontSize = 15.sp)
            Spacer(modifier = Modifier.height(8.dp))
        }

        items(listOf("தக்காளி (Tomato)", "நிலக்கடலை (Groundnut)", "மக்காச்சோளம் (Maize)")) { crop ->
            Card(
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier.fillMaxWidth().padding(vertical = 6.dp)
            ) {
                Column(modifier = Modifier.padding(14.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text(crop, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                        Surface(shape = RoundedCornerShape(8.dp), color = Color(0xFFE8F5E9)) {
                            Text("Suitability: 92%", color = ForestGreen, fontSize = 12.sp, modifier = Modifier.padding(4.dp))
                        }
                    }
                    Text("Expected Harvest Window: Feb 2027 (105 Days)", fontSize = 12.sp, color = Color.DarkGray)
                    Divider(modifier = Modifier.padding(vertical = 8.dp))
                    
                    Text("Harvest Price Scenarios (அறுவடை விலை கணிப்பு):", fontWeight = FontWeight.Medium, fontSize = 13.sp)
                    Row(modifier = Modifier.fillMaxWidth().padding(top = 4.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                        ScenarioTag("Pessimistic", "₹8.0/kg", AlertRed)
                        ScenarioTag("Normal", "₹16.0/kg", ForestGreen)
                        ScenarioTag("Optimistic", "₹26.0/kg", Color(0xFF0D47A1))
                    }
                    Spacer(modifier = Modifier.height(6.dp))
                    Text("Estimated Net Profit (Normal): ₹1,47,000", fontWeight = FontWeight.Bold, color = ForestGreen)
                }
            }
        }
    }
}

@Composable
fun ScenarioTag(name: String, price: String, color: Color) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(name, fontSize = 10.sp, color = Color.Gray)
        Text(price, fontWeight = FontWeight.Bold, fontSize = 13.sp, color = color)
    }
}

@Composable
fun ProtectScreen() {
    LazyColumn(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        item {
            Card(
                colors = CardDefaults.cardColors(containerColor = Color(0xFFE8F5E9)),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                    Text("🌤️", fontSize = 32.sp)
                    Spacer(modifier = Modifier.width(16.dp))
                    Column {
                        Text("Dindigul Weather: 28.5°C • Humidity 75%", fontWeight = FontWeight.Bold)
                        Text("24h Rainfall: 0.0mm • Soil Moisture: Adequate", fontSize = 13.sp, color = Color.DarkGray)
                    }
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
            Text("Active Warnings & Advisories", fontWeight = FontWeight.Bold, fontSize = 16.sp)
            Spacer(modifier = Modifier.height(8.dp))
        }

        item {
            Card(
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(14.dp)) {
                    Surface(shape = RoundedCornerShape(6.dp), color = Color(0xFFFFF3E0)) {
                        Text("⚠️ Early Blight Warning (இலைக்கருகல்)", color = AmberWarning, fontWeight = FontWeight.Bold, fontSize = 12.sp, modifier = Modifier.padding(4.dp))
                    }
                    Spacer(modifier = Modifier.height(6.dp))
                    Text("High humidity creates fungal infection risks for tomato crops.", fontSize = 13.sp)
                    Text("Action: Spray Pseudomonas fluorescens (0.2%) during morning hours.", fontWeight = FontWeight.SemiBold, fontSize = 12.sp, color = ForestGreen)
                }
            }
        }
    }
}

@Composable
fun RecoverScreen() {
    LazyColumn(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        item {
            Card(
                colors = CardDefaults.cardColors(containerColor = Color(0xFFFFEBEE)),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("⏱️", fontSize = 24.sp)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("PMFBY 72-Hour Calamity Timer", fontWeight = FontWeight.Bold, color = AlertRed, fontSize = 16.sp)
                    }
                    Text("Under PMFBY rules, localized crop losses must be reported within 72 hours.", fontSize = 12.sp, color = Color.DarkGray)
                    Spacer(modifier = Modifier.height(12.dp))
                    LinearProgressIndicator(
                        progress = { 0.65f },
                        modifier = Modifier.fillMaxWidth().height(8.dp),
                        color = AlertRed,
                        trackColor = Color(0xFFFFCDD2)
                    )
                    Spacer(modifier = Modifier.height(6.dp))
                    Text("Time Remaining: 48.0 Hours (URGENT)", fontWeight = FontWeight.Bold, color = AlertRed, fontSize = 13.sp)
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
            Button(
                onClick = { /* Capture geotagged photos */ },
                colors = ButtonDefaults.buttonColors(containerColor = AlertRed),
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("📷 Report Loss & Capture Geotagged Photos")
            }
            Spacer(modifier = Modifier.height(12.dp))
            Button(
                onClick = { /* Generate Dossier PDF */ },
                colors = ButtonDefaults.buttonColors(containerColor = ForestGreen),
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("📄 Generate PMFBY Claim Dossier (அறிக்கை)")
            }
            Spacer(modifier = Modifier.height(12.dp))
            Text("PMFBY Toll-Free Helpline: 14447 / 1800-180-1551", fontWeight = FontWeight.Bold, fontSize = 13.sp)
        }
    }
}

@Composable
fun ReconnectScreen() {
    LazyColumn(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        item {
            Text("Alternative Industrial Buyer Discovery (சந்தை மீட்பு)", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = ForestGreen)
            Spacer(modifier = Modifier.height(8.dp))
            Text("Connect rain-blemished or cracked produce with puree and paste factories.", fontSize = 12.sp, color = Color.DarkGray)
            Spacer(modifier = Modifier.height(12.dp))
            Card(
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(14.dp)) {
                    Text("Distressed Produce: Tomato (3,500 kg)", fontWeight = FontWeight.Bold)
                    Text("Grade: Grade B (Suitable for Puree/Sauce)", color = SageGreen, fontWeight = FontWeight.SemiBold, fontSize = 13.sp)
                    Text("Food Safety Check: PASSED (Non-rotten, no bacterial decay)", fontSize = 11.sp, color = Color.Gray)
                    Divider(modifier = Modifier.padding(vertical = 8.dp))
                    Text("Verified Buyer Offers (சரிபார்க்கப்பட்ட விலைப்புள்ளிகள்):", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                    Spacer(modifier = Modifier.height(6.dp))
                    
                    Text("1. Nilakottai Puree Processing Ltd", fontWeight = FontWeight.SemiBold)
                    Text("Offered: ₹11.50/kg • Transport: -₹1.20/kg", fontSize = 12.sp)
                    Text("Net Realization: ₹10.30/kg • Total Payout: ₹36,050", fontWeight = FontWeight.Bold, color = ForestGreen)
                    
                    Divider(modifier = Modifier.padding(vertical = 8.dp))
                    Text("2. Kaveri Valley Condiments (Farmgate Pickup)", fontWeight = FontWeight.SemiBold)
                    Text("Offered: ₹10.80/kg • Transport: Free Pickup", fontSize = 12.sp)
                    Text("Net Realization: ₹10.80/kg • Total Payout: ₹37,800", fontWeight = FontWeight.Bold, color = ForestGreen)
                }
            }
        }
    }
}
