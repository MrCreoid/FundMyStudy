# 🎓 FundMyStudy

> Bridging the gap for rural Indian students to access government scholarships through smart matching and simplified application processes.

**Live Demo:** [https://fundmystudy.onrender.com](https://fundmystudy.onrender.com)

## 🚀 Features

- **🤖 Smart Eligibility Matching**: Automatically matches students with verified government scholarships based on their profile.
- **🔐 Secure Authentication**: Firebase-powered login and signup system.
- **📄 Profile Management**: Comprehensive student profile including caste, income, and course details.
- **🌙 Dark Mode**: Fully supported dark theme with memory persistence.
- **🎨 Glassmorphism UI**: Modern, clean, and responsive interface designed for readability.
- **☁️ Cloud Ready**: Backend and Frontend optimized for deployment on Render.

## 🛠️ Tech Stack

### Frontend
- **React 18** (Vite)
- **Firebase Auth**
- **CSS3 Variables** (Theming)

### Backend
- **FastAPI** (Python 3.10+)
- **Uvicorn**
- **Google Cloud Firestore** (Database)

## ⚡ Quick Start (Local Development)

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- Firebase Project Credentials

### 1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run the server (default port 8000)
uvicorn app:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install

# Run the dev server (default port 5173)
npm run dev
```

### 3. Environment Configuration
The application automatically detects valid API endpoints:
- **Localhost**: Defaults to `http://localhost:8000`
- **Top-Level Domain**: Defaults to `https://fundmystudy-1.onrender.com`

You can validly override this by creating a `.env` file in `frontend/`:
```env
VITE_API_URL=http://your-custom-backend-url.com
```

## 🚀 Deployment (Render)

This project is configured for seamless deployment on Render.

1.  **Backend Service**:
    *   Build Command: `pip install -r requirements.txt`
    *   Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
    *   Environment Variables:
        *   `FIREBASE_CREDENTIALS` (JSON string of service account)
        *   `PORT` (automatically set by Render)

2.  **Frontend Static Site**:
    *   Build Command: `npm run build`
    *   Publish Directory: `dist`
    *   **Rewrite Rule**: Source `/*` -> Destination `/index.html` (for SPA routing)

## 👥 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License
[MIT](https://choosealicense.com/licenses/mit/)
