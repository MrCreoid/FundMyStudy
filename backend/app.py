from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

# Update import paths
from routes import profile, scholarships
from services.firebase_admin import initialize_firebase

app = FastAPI(title="FundMyStudy Backend", version="1.0.0")

# Initialize Firebase
initialize_firebase()

# CORS configuration - UPDATE WITH YOUR FRONTEND URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://fundmystudy-frontend.onrender.com",  # Your frontend URL
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(profile.router)
app.include_router(scholarships.router)

@app.get("/")
def root():
    return {"message": "FundMyStudy Backend API", "status": "running"}

@app.get("/scholarships")
async def get_scholarships():
    # Return mock data for now
    return [
        {"id": 1, "name": "Scholarship 1", "amount": 5000},
        {"id": 2, "name": "Scholarship 2", "amount": 10000}
    ]

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)