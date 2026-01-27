# app.py
from fastapi import FastAPI
import os

app = FastAPI()

# Get the port from environment variable (Render provides this)
PORT = int(os.getenv("PORT", 8000))

# Root endpoint - THIS WILL DEFINITELY WORK
@app.get("/")
def read_root():
    return {
        "message": "FundMyStudy Backend is running!",
        "status": "active",
        "api": "v1.0",
        "endpoints": ["/", "/health", "/test", "/api/scholarships"]
    }

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "FundMyStudy API"}

# Test endpoint
@app.get("/test")
def test_endpoint():
    return {"test": "success", "message": "API is working"}

# Scholarships endpoint
@app.get("/api/scholarships")
def get_scholarships():
    return [
        {"id": 1, "name": "Merit Scholarship", "amount": 5000},
        {"id": 2, "name": "Need-Based Grant", "amount": 10000},
        {"id": 3, "name": "Research Fellowship", "amount": 15000}
    ]

# User endpoint
@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": "John Doe", "email": "john@example.com"}

# Print startup message
print(f"✅ Server starting on port {PORT}")
print(f"✅ Root URL: http://0.0.0.0:{PORT}/")