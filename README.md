# UID
eDYCUg5suEPgPVOZLysl1qyIqNR2

# Firebase Console

// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCzmKUJt7XD7M9MjMxltn22ceps1Yt186Y",
  authDomain: "fundmystudy-527.firebaseapp.com",
  projectId: "fundmystudy-527",
  storageBucket: "fundmystudy-527.firebasestorage.app",
  messagingSenderId: "389826221589",
  appId: "1:389826221589:web:6eda2b3a3890a759d5601c",
  measurementId: "G-BQL5M24Q9V"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);


# SCRAPE MANUALLY (run in root)

export GOOGLE_CLOUD_PROJECT=fundmystudy-527
python scraper/main.py
