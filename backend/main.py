from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, citizen, worker, admin, pwa

app = FastAPI(
    title="Clean Connect Smart India Portal", 
    version="3.0.0",
    description="Multi-role Smart Waste platform with 36-hour deadlines and scoped PWAs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(citizen.router)
app.include_router(worker.router)
app.include_router(admin.router)
app.include_router(pwa.router)
