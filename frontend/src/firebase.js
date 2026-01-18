import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCzmKUJt7XD7M9MjMxltn22ceps1Yt186Y",
  authDomain: "fundmystudy-527.firebaseapp.com",
  projectId: "fundmystudy-527",
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
