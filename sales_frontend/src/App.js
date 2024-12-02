import React, { useState } from "react";

function App() {
  const [response, setResponse] = useState(null);
  const [file, setFile] = useState(null);

  // Funktion zum Hochladen der Datei
  const handleFileUpload = async () => {
    if (!file) {
      alert("Bitte wählen Sie eine Datei aus, bevor Sie hochladen.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/upload_data/", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`HTTP-Fehler! Status: ${res.status}`);
      }

      const data = await res.json();
      console.log("Erhaltene Daten:", data); // Debugging
      setResponse(data);
    } catch (error) {
      console.error("Fehler beim Hochladen der Datei:", error);
      setResponse({ error: "Fehler beim Hochladen der Datei." });
    }
  };

  // Funktion für das Setzen der Datei
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  return (
    <div className="App">
      <h1>Sales Dashboard</h1>

      {/* Datei-Upload */}
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={handleFileUpload}>Datei hochladen</button>

      {/* Anzeige der Antwort vom Backend */}
      {response ? (
        response.error ? (
          <p>Fehler: {response.error}</p>
        ) : (
          <div>
            <h2>Ergebnisse</h2>
            <p>Status: {response.status}</p>
            <p>Verarbeitete Zeilen: {response.rows}</p>

            {/* Anzeige numerischer Spalten */}
            {response.numerical_columns &&
            Object.keys(response.numerical_columns).length > 0 ? (
              <div>
                <h3>Numerische Spalten</h3>
                {Object.keys(response.numerical_columns).map((column) => (
                  <div key={column}>
                    <h4>{column}</h4>
                    <p>Durchschnitt: {response.numerical_columns[column].mean}</p>
                    <p>Standardabweichung: {response.numerical_columns[column].std}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p>Keine numerischen Spalten gefunden.</p>
            )}

            {/* Anzeige von Anomalien */}
            {response.anomalies && response.anomalies.length > 0 ? (
              <div>
                <h3>Anomalien</h3>
                <ul>
                  {response.anomalies.map((anomaly, index) => (
                    <li key={index}>
                      <strong>Zeile:</strong> {anomaly.row}, <strong>Wert:</strong>{" "}
                      {anomaly.value}, <strong>Grund:</strong> {anomaly.reason}
                    </li>
                  ))}
                </ul>
              </div>
            ) : (
              <p>Keine Anomalien gefunden.</p>
            )}
          </div>
        )
      ) : (
        <p>Laden...</p>
      )}
    </div>
  );
}

export default App;
