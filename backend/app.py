from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import os

# Update import paths
try:
    from routes import profile, scholarships
    from services.firebase_admin import initialize_firebase
except ImportError as e:
    print(f"Import error: {e}")
    # Create dummy modules for testing
    class DummyRouter:
        def __init__(self):
            self.routes = []
    profile = type('obj', (object,), {'router': DummyRouter()})
    scholarships = type('obj', (object,), {'router': DummyRouter()})
    
    def initialize_firebase():
        print("Firebase initialization skipped (dummy function)")

# Initialize FastAPI app
app = FastAPI(
    title="FundMyStudy Backend",
    version="1.0.0",
    description="Backend API for FundMyStudy scholarship platform",
)

# Get frontend URL from environment with fallback
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://fundmystudy.onrender.com")
PORT = int(os.getenv("PORT", 8000))

# Initialize Firebase
try:
    initialize_firebase()
    print("Firebase initialized successfully")
except Exception as e:
    print(f"Firebase initialization error: {e}")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://localhost:5173",
        "http://localhost:3000",
        "*"  # Allow all origins for testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic root endpoint that should definitely work
@app.get("/")
def root():
    return {
        "message": "FundMyStudy Backend API is running",
        "status": "online",
        "version": "1.0.0",
        "timestamp": time.time(),
        "endpoints": [
            "/health",
            "/api/v1/mock/scholarships",
            "/api/v1/eligible",
            "/api/v1/info",
            "/api/docs"
        ]
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FundMyStudy Backend",
        "timestamp": time.time()
    }

# Test endpoint
@app.get("/test")
def test_endpoint():
    return {"message": "Test endpoint is working", "success": True}

# Mock data endpoint
@app.get("/api/v1/mock/scholarships")
async def get_mock_scholarships():
    return [
        {"id": 1, "name": "Merit Scholarship", "amount": 5000, "deadline": "2024-12-31"},
        {"id": 2, "name": "Need-based Grant", "amount": 10000, "deadline": "2024-11-30"},
        {"id": 3, "name": "Research Fellowship", "amount": 15000, "deadline": "2024-10-15"}
    ]

# Eligibility endpoint
@app.get("/api/v1/eligible")
async def check_eligibility():
    return {
        "message": "Eligibility check endpoint",
        "status": "active",
        "description": "This endpoint will check scholarship eligibility based on user profile",
        "data": []
    }

# Server info endpoint
@app.get("/api/v1/info")
def server_info():
    return {
        "service": "FundMyStudy Backend API",
        "version": "1.0.0",
        "environment": "production",
        "frontend_url": FRONTEND_URL,
        "port": PORT,
        "api_base": "/api/v1"
    }

# Try to include routers if they exist
try:
    app.include_router(profile.router, prefix="/api/v1")
    app.include_router(scholarships.router, prefix="/api/v1")
    print("Routers included successfully")
except Exception as e:
    print(f"Router inclusion error: {e}")

# Startup message
print(f"Server starting on port {PORT}")
print(f"Frontend URL: {FRONTEND_URL}")
print(f"Root endpoint: http://localhost:{PORT}/")
print(f"Health check: http://localhost:{PORT}/health")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")