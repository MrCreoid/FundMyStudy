import { initializeApp } from "firebase/app";
import { getAuth, signInWithEmailAndPassword } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCzmKUJt7XD7M9MjMxltn22ceps1Yt186Y",
  authDomain: "fundmystudy-527.firebaseapp.com",
  projectId: "fundmystudy-527",
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

async function getToken() {
  const userCredential = await signInWithEmailAndPassword(
    auth,
    "test@student.com",
    "test1234"
  );

  const token = await userCredential.user.getIdToken();
  console.log(token);
}

getToken();
