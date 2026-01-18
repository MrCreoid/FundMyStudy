export default function Navbar({ loggedIn, setPage }) {
  return (
    <nav>
      <div><strong>FundMyStudy</strong></div>
      <div>
        <a onClick={() => setPage("home")}>Home</a>
        {!loggedIn && <a onClick={() => setPage("login")}>Login</a>}
        {loggedIn && <a onClick={() => setPage("profile")}>Profile</a>}
        {loggedIn && <a onClick={() => setPage("scholarships")}>Scholarships</a>}
      </div>
    </nav>
  );
}