from fastapi import APIRouter, HTTPException
from ..db import db
from ..sla_manager import SLAManager

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])

@router.get("/monitor")
def admin_global_monitor(admin_id: str):
    """Provides administrators with full operational oversight of the system."""
    admin = db.users.get(admin_id)
    if not admin or admin["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Administrative authorization required.")

    total_complaints = len(db.complaints)
    resolved_count = sum(1 for c in db.complaints.values() if c["status"] == "RESOLVED")
    sla_violations = sum(1 for c in db.complaints.values() if c["status"] == "FAILED_SLA")
    
    active_sla_breaches = 0
    for c in db.complaints.values():
        if c["status"] in {"PENDING", "ASSIGNED"} and not SLAManager.check_sla_compliance(c["deadline_at"]):
            active_sla_breaches += 1

    return {
        "metrics": {
            "total_complaints": total_complaints,
            "resolved_complaints": resolved_count,
            "sla_violations": sla_violations,
            "active_overdue_complaints": active_sla_breaches,
            "smart_dustbins_count": len(db.dustbins)
        },
        "all_complaints": list(db.complaints.values()),
        "users_directory": list(db.users.values())
    }
