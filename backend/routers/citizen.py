import time
import random
from fastapi import APIRouter, HTTPException
from ..models import ComplaintSubmissionIn
from ..db import db
from ..validators import LocationParser
from ..sla_manager import SLAManager
from ..antigravity_client import AntigravityAPIClient

router = APIRouter(prefix="/api/v1/citizen", tags=["Citizen"])

@router.post("/complaints")
def submit_complaint(payload: ComplaintSubmissionIn):
    """Ingests citizen complaints, verifies geotags, and logs coordinates."""
    citizen = db.users.get(payload.citizen_id)
    if not citizen or citizen["role"] != "CITIZEN":
        raise HTTPException(status_code=403, detail="Only registered citizens can submit complaints.")

    if not LocationParser.verify_and_extract_metadata(payload.image_base64):
        raise HTTPException(
            status_code=400, 
            detail="Verification error: The uploaded image does not contain native GPS geotags."
        )

    sla_time = SLAManager.calculate_sla_window()
    complaint_id = f"cmp-{int(time.time())}-{random.randint(1000, 9999)}"

    complaint_record = {
        "id": complaint_id,
        "citizen_id": payload.citizen_id,
        "worker_id": None,
        "latitude": payload.latitude,
        "longitude": payload.longitude,
        "description": payload.description,
        "status": "PENDING",
        "proof_image_url": None,
        "created_at": sla_time["created_at"],
        "deadline_at": sla_time["deadline_at"],
        "completed_at": None
    }

    db.complaints[complaint_id] = complaint_record

    client = AntigravityAPIClient(project_id="cleanconnect-sih")
    log_msg = f"Complaint {complaint_id} filed by {payload.citizen_id}. SLA active until {sla_time['deadline_at']}."
    try:
        for _ in client.log_operations(log_msg):
            pass
    except Exception:
        pass

    return {
        "complaint_id": complaint_id,
        "status": "REGISTERED",
        "deadline": sla_time["deadline_at"].isoformat()
    }

@router.get("/map-assets")
def get_citizen_dashboard_assets():
    """Returns smart dustbin layouts and local municipal directory contacts."""
    return {
        "dustbins": db.dustbins,
        "authorities": db.authorities
    }
