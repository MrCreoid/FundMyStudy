from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import os

# Update import paths
from routes import profile, scholarships
from services.firebase_admin import initialize_firebase

# Initialize FastAPI app with enhanced metadata
app = FastAPI(
    title="FundMyStudy Backend",
    version="1.0.0",
    description="Backend API for FundMyStudy scholarship platform",
    contact={
        "name": "FundMyStudy Team",
        "email": "contact@fundmystudy.com",
    },
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Get frontend URL from environment with fallback
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://fundmystudy.onrender.com")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Initialize Firebase
initialize_firebase()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Process time middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# Routes with API version prefix
app.include_router(profile.router, prefix="/api/v1")
app.include_router(scholarships.router, prefix="/api/v1")

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "FundMyStudy Backend API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/api/docs"
    }

# Mock data endpoint (avoiding conflict with actual scholarships route)
@app.get("/api/v1/mock/scholarships")
async def get_mock_scholarships():
    """Temporary mock scholarships endpoint for testing"""
    return [
        {"id": 1, "name": "Scholarship 1", "amount": 5000},
        {"id": 2, "name": "Scholarship 2", "amount": 10000}
    ]

# Placeholder eligibility endpoint
@app.get("/api/v1/eligible")
async def check_eligibility():
    """Eligibility endpoint placeholder"""
    return {
        "message": "Eligibility endpoint placeholder",
        "endpoint": "This endpoint will be implemented soon",
        "data": []
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "FundMyStudy Backend"
    }

# Server information endpoint
@app.get("/api/v1/info")
def server_info():
    return {
        "service": "FundMyStudy Backend",
        "version": "1.0.0",
        "environment": "development" if DEBUG else "production",
        "frontend_url": FRONTEND_URL
    }