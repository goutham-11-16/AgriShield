from datetime import date, datetime, timedelta
from typing import List, Dict, Any, Optional
import uuid
from backend.app.schemas.schemas import DisasterReportCreate, DisasterReportResponse

# Tamil Nadu SDRF Input Subsidy Norms (Revised as per CRA Disaster Relief Norms)
# Rainfed land: ~₹8,500/ha (~₹3,440/acre)
# Assured Irrigated land: ~₹17,000/ha (~₹6,880/acre)
# Perennial horticultural crops: ~₹22,500/ha (~₹9,105/acre)
# Minimum damage threshold for SDRF eligibility: 33% crop loss
SDRF_IRRIGATED_RELIEF_PER_ACRE = 6880.0

def process_disaster_report(report: DisasterReportCreate) -> DisasterReportResponse:
    report_id = f"DR-{str(uuid.uuid4())[:8].upper()}"
    today = date.today()
    
    # Calculate days/hours elapsed since incident
    days_elapsed = (today - report.incident_date).days
    # Estimate total hours assuming loss occurred at 06:00 AM on incident date
    hours_elapsed = max(0.0, float(days_elapsed * 24.0))
    
    pmfby_limit_hours = 72.0
    is_within_72h = hours_elapsed <= pmfby_limit_hours
    hours_remaining = max(0.0, pmfby_limit_hours - hours_elapsed)
    
    urgency_status = "URGENT - Within 72h Window" if is_within_72h else "ESCALATED - Past 72h Standard Deadline"
    
    # Calculate estimated SDRF input subsidy relief if damage >= 33%
    sdrf_relief = 0.0
    if report.estimated_damage_percentage >= 33.0:
        sdrf_relief = round(report.affected_area_acres * SDRF_IRRIGATED_RELIEF_PER_ACRE, 2)
        
    checklist_en = [
        "1. Retain timestamped, geotagged photographs of the submerged/damaged crop field.",
        "2. Keep your Aadhaar Card, Bank Passbook, Land Document (Patta/Chitta), and PMFBY Sowing Certificate ready.",
        "3. Inform your local Village Administrative Officer (VAO) or Block Assistant Director of Agriculture (ADA).",
        "4. Call the National PMFBY Toll-Free Helpline at 14447 or 1800-180-1551 to register loss intimation token.",
        "5. Submit the AgriShield Loss Claim Dossier at your nearest Primary Agricultural Cooperative Credit Society (PACCS) or CSC center."
    ]
    
    checklist_ta = [
        "1. சேதமடைந்த அல்லது மூழ்கிய பயிர் நிலத்தின் நேர முத்திரை மற்றும் ஜி.பி.எஸ் இருப்பிட புகைப்படங்களை பத்திரப்படுத்தவும்.",
        "2. ஆதார் அட்டை, வங்கி சேமிப்பு புத்தகம், நில ஆவணம் (பட்டா/சிட்டா) மற்றும் பயிர் காப்பீட்டு ரசீதை தயாராக வைத்திருக்கவும்.",
        "3. உங்கள் கிராம நிர்வாக அலுவலர் (VAO) அல்லது வட்டார வேளாண்மை உதவி இயக்குநரிடம் (ADA) உடனே தெரிவிக்கவும்.",
        "4. மத்திய அரசின் இலவச பயிர் காப்பீட்டு உதவி எண் 14447 அல்லது 1800-180-1551 ஐ அழைத்து இழப்பு பதிவு எண்ணை (Token) பெறவும்.",
        "5. அக்ரிஷீல்ட் (AgriShield) தயார் செய்த இழப்பீட்டு அறிக்கையை உங்கள் தொடக்க வேளாண்மை கூட்டுறவு சங்கம் (PACCS) அல்லது இ-சேவை மையத்தில் சமர்ப்பிக்கவும்."
    ]

    return DisasterReportResponse(
        report_id=report_id,
        crop_name=report.crop_name,
        incident_date=report.incident_date,
        is_within_72h_pmfby=is_within_72h,
        hours_remaining_for_pmfby=round(hours_remaining, 1),
        urgency_status=urgency_status,
        claim_dossier_ready=True,
        sdrf_estimated_relief_inr=sdrf_relief,
        pmfby_helpline="14447 (National Toll-Free) / 1800 180 1551",
        official_action_checklist=checklist_en,
        official_action_checklist_ta=checklist_ta
    )
