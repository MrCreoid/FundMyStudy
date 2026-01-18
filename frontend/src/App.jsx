import { useState } from "react";
import Navbar from "./components/Navbar1";
import Home from "./pages/Home";
import Login from "./pages/Login1";
import Profile from "./pages/Profile1";
import Scholarships from "./pages/Scholarships";

function App() {
  const [token, setToken] = useState(null);
  const [page, setPage] = useState("home");

  return (
    <>
      <Navbar loggedIn={!!token} setPage={setPage} />

      {page === "home" && <Home />}
      {page === "login" && <Login onLogin={(t) => {
        setToken(t);
        setPage("profile");
      }} />}
      {page === "profile" && token && <Profile token={token} />}
      {page === "scholarships" && token && <Scholarships token={token} />}
    </>
  );
}

export default App;
