from pydantic import BaseModel, Field

class CitizenRegistrationIn(BaseModel):
    name: str
    email: str
    phone: str
    role: str = Field(..., description="CITIZEN, WORKER, or ADMIN")

class ComplaintSubmissionIn(BaseModel):
    citizen_id: str
    latitude: float = Field(..., ge=-90.0, le=90.0, json_schema_extra={"example": 28.6139})
    longitude: float = Field(..., ge=-180.0, le=180.0, json_schema_extra={"example": 77.2090})
    image_base64: str = Field(..., description="Base64 encoded photo with EXIF geotags")
    description: str

class ResolutionSubmissionIn(BaseModel):
    worker_id: str
    proof_image_base64: str
