from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import profile, scholarships
import services.firebase_admin

app = FastAPI(
    title="FundMyStudy Backend API",
    description="Backend API for FundMyStudy scholarship platform",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # React dev server
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(profile.router)
app.include_router(scholarships.router)

@app.get("/")
async def root():
    return {
        "message": "FundMyStudy Backend API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "profiles": "/profiles",
            "scholarships": "/scholarships"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fundmystudy-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )