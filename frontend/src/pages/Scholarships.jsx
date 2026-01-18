import { useEffect, useState } from "react";

export default function Scholarships({ token }) {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/scholarships/eligible", {
      headers: { "Authorization": `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(setData);
  }, []);

  return (
    <div className="container">
      <h2>Eligible Scholarships</h2>

      {data.length === 0 && <p>No eligible scholarships found.</p>}

      {data.map(s => (
        <div className="card" key={s.scholarshipId}>
          <h3>{s.name}</h3>
          <p><strong>Provider:</strong> {s.provider}</p>
          <p><strong>Deadline:</strong> {s.deadline}</p>
          <p><strong>Eligibility Score:</strong> {s.score}</p>
          <a href={s.apply_link} target="_blank">
            <button>Apply Now</button>
          </a>
        </div>
      ))}
    </div>
  );
}