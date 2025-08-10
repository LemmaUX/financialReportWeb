// Esqueleto de App React para frontend
import React, { useState } from "react";
import axios from "axios";

function App() {
  const [asset, setAsset] = useState("");
  const [data, setData] = useState(null);
  const [greeting, setGreeting] = useState("");

  const fetchGreeting = async () => {
    try {
      const res = await axios.get("http://localhost:8000/hello");
      setGreeting(res.data.message);
    } catch (error) {
      setGreeting("Error al cargar el saludo");
    }
  };

  const fetchReport = async () => {
    const res = await axios.get("http://localhost:8000/reports", {
      params: { asset, from_date: "2024-01-01", to_date: "2024-06-30" },
      headers: { Authorization: "Bearer fake-token" }
    });
    setData(res.data);
  };

  return (
    <div style={{padding: "20px", fontFamily: "Arial, sans-serif"}}>
      <h1>Reportes Financieros</h1>
      
      <div style={{marginBottom: "20px", padding: "10px", backgroundColor: "#f0f8ff", border: "1px solid #ccc", borderRadius: "5px"}}>
        <button onClick={fetchGreeting} style={{marginBottom: "10px"}}>Mostrar Saludo</button>
        {greeting && <div style={{fontSize: "18px", color: "#2e7d32"}}>{greeting}</div>}
      </div>

      <div>
        <input value={asset} onChange={e => setAsset(e.target.value)} placeholder="Asset"/>
        <button onClick={fetchReport}>Buscar</button>
        <pre>{JSON.stringify(data, null, 2)}</pre>
      </div>
    </div>
  );
}

export default App;
