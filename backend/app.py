from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import profile, scholarships
from services import firebase_admin  # ensures Firebase init

app = FastAPI()

# CORS MUST be added BEFORE routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],     # <-- THIS enables OPTIONS
    allow_headers=["*"],
)

# Routes
app.include_router(profile.router)
app.include_router(scholarships.router)
