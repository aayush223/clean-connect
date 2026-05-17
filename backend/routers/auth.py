import time
import random
from fastapi import APIRouter, HTTPException
from ..models import CitizenRegistrationIn
from ..db import db

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.post("/register")
def register_user(payload: CitizenRegistrationIn):
    """Registers new users and assigns their operational roles."""
    user_id = f"usr-{int(time.time())}-{random.randint(100, 999)}"
    role_clean = payload.role.upper()
    if role_clean not in {"CITIZEN", "WORKER", "ADMIN"}:
        raise HTTPException(status_code=400, detail="Invalid operational role provided.")

    db.users[user_id] = {
        "id": user_id,
        "name": payload.name,
        "email": payload.email,
        "phone": payload.phone,
        "role": role_clean,
        "fcm_token": f"fcm-token-mock-{user_id}"
    }
    return {"user_id": user_id, "role": role_clean, "status": "SUCCESS"}
