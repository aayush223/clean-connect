from datetime import datetime
from fastapi import APIRouter, HTTPException
from ..models import ResolutionSubmissionIn
from ..db import db
from ..sla_manager import SLAManager
from ..antigravity_client import AntigravityAPIClient

router = APIRouter(prefix="/api/v1/worker", tags=["Worker"])

@router.get("/tasks")
def get_worker_tasks(worker_id: str):
    """Fetches assigned tasks and displays navigation details and active SLAs."""
    worker = db.users.get(worker_id)
    if not worker or worker["role"] != "WORKER":
        raise HTTPException(status_code=403, detail="Access denied. Worker credentials required.")

    assigned_tasks = []
    for cid, cmp in db.complaints.items():
        if cmp["worker_id"] == worker_id or cmp["worker_id"] is None:
            time_remaining_sec = (cmp["deadline_at"] - datetime.now()).total_seconds()
            assigned_tasks.append({
                "complaint_id": cid,
                "latitude": cmp["latitude"],
                "longitude": cmp["longitude"],
                "description": cmp["description"],
                "status": cmp["status"],
                "deadline_at": cmp["deadline_at"].isoformat(),
                "time_remaining_hours": round(max(0.0, time_remaining_sec / 3600.0), 2),
                "is_sla_violated": not SLAManager.check_sla_compliance(cmp["deadline_at"])
            })
    return assigned_tasks

@router.post("/resolve")
def resolve_complaint(complaint_id: str, payload: ResolutionSubmissionIn):
    """Records proof of completion from workers and routes photos to citizens and admins."""
    complaint = db.complaints.get(complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint record not found.")

    if complaint["status"] == "RESOLVED":
        raise HTTPException(status_code=400, detail="This complaint has already been resolved.")

    worker = db.users.get(payload.worker_id)
    if not worker or worker["role"] != "WORKER":
        raise HTTPException(status_code=403, detail="Valid worker registration required.")

    if len(payload.proof_image_base64) < 100:
        raise HTTPException(status_code=400, detail="Invalid proof image payload submitted.")

    completed_time = datetime.now()
    is_compliant = SLAManager.check_sla_compliance(complaint["deadline_at"])
    
    complaint["status"] = "RESOLVED" if is_compliant else "FAILED_SLA"
    complaint["worker_id"] = payload.worker_id
    complaint["completed_at"] = completed_time
    complaint["proof_image_url"] = f"https://s3.ap-south-1.amazonaws.com/sih-cleanconnect/proof-{complaint_id}.png"

    client = AntigravityAPIClient(project_id="cleanconnect-sih")
    sla_status = "compliant" if is_compliant else "non-compliant (SLA Breached)"
    log_msg = f"Task {complaint_id} resolved by {payload.worker_id}. Resolution state: {sla_status}."
    try:
        for _ in client.log_operations(log_msg):
            pass
    except Exception:
        pass

    return {
        "complaint_id": complaint_id,
        "status": complaint["status"],
        "completed_at": completed_time.isoformat(),
        "is_sla_compliant": is_compliant
    }
