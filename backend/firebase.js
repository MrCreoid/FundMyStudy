import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCzmKUJt7XD7M9MjMxltn22ceps1Yt186Y",
  authDomain: "fundmystudy-527.firebaseapp.com",
  projectId: "fundmystudy-527",
  storageBucket: "fundmystudy-527.firebasestorage.app",
  messagingSenderId: "389826221589",
  appId: "1:389826221589:web:6eda2b3a3890a759d5601c",
  measurementId: "G-BQL5M24Q9V"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);