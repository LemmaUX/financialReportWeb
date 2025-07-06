// Esqueleto de App React para frontend
import React, { useState } from "react";
import axios from "axios";

function App() {
  const [asset, setAsset] = useState("");
  const [data, setData] = useState(null);

  const fetchReport = async () => {
    const res = await axios.get("http://localhost:8000/reports", {
      params: { asset, from_date: "2024-01-01", to_date: "2024-06-30" },
      headers: { Authorization: "Bearer fake-token" }
    });
    setData(res.data);
  };

  return (
    <div>
      <input value={asset} onChange={e => setAsset(e.target.value)} placeholder="Asset"/>
      <button onClick={fetchReport}>Buscar</button>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

export default App;
