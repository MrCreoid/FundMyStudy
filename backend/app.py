# app.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import scholarships, profile, auth

app = FastAPI()

# Server configuration
PORT = int(os.getenv("PORT", 8000))

# CORS Configuration
# Allow requests from local frontend and potential production domains
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(scholarships.router)
app.include_router(profile.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {
        "status": "active",
        "service": "FundMyStudy API",
        "version": "1.0",
        "endpoints": [
            "/", 
            "/health", 
            "/scholarships/eligible",
            "/profiles/me",
            "/auth/test"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/test")
def test_endpoint():
    return {"status": "success", "message": "API is operational"}

if __name__ == "__main__":
    import uvicorn
    # Host must be 0.0.0.0 for Render compatibility
    uvicorn.run(app, host="0.0.0.0", port=PORT)
else:
    print(f"Server initialized on port {PORT}")