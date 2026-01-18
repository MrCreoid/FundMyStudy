from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import profile, scholarships

app = FastAPI(title="FundMyStudy Backend", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)