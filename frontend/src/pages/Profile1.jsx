export default function Profile({ token }) {
  const saveProfile = async () => {
    await fetch("http://127.0.0.1:8000/profiles", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({
        name: "John Doe",
        income: 250000,
        caste: "OBC",
        category: "Minority",
        course: "B.Tech",
        state: "Maharashtra",
        marks: 87.5
      })
    });
    alert("Profile saved");
  };

  return (
    <div className="container">
      <div className="card">
        <h2>Student Profile</h2>
        <p>Fill your details to check scholarship eligibility.</p>
        <button onClick={saveProfile}>Save Profile</button>
      </div>
    </div>
  );
}