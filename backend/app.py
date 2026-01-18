from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import profile, scholarships, auth  # Add auth import
import os

# Initialize Firebase
import services.firebase_admin

app = FastAPI(title="FundMyStudy Backend", version="1.0.0")

# CORS configuration - Allow all for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router)  # Add auth router
app.include_router(profile.router)
app.include_router(scholarships.router)

@app.get("/")
def root():
    return {"message": "FundMyStudy Backend API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)