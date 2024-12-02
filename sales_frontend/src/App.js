import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);

  // Funktion zum Verarbeiten der Dateiauswahl
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    console.log("Selected file:", e.target.files[0]);
  };

  // Funktion zum Hochladen der Datei
  const handleUpload = async () => {
    if (!file) {
      alert('Bitte wählen Sie eine Datei aus.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('http://127.0.0.1:8000/upload_data/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Überprüfe, was genau vom Backend zurückkommt
      console.log("Backend response:", res.data);

      // Wenn die Antwort eine erfolgreiche Nachricht enthält
      if (res.data.status === "Daten hochgeladen") {
        setResponse(res.data); // Erfolgreiche Antwort
      } else {
        setResponse({ error: "Unbekannter Fehler beim Hochladen der Datei" });
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      setResponse({ error: 'Error uploading file, please try again.' });
    }
  };

  return (
    <div className="App">
      <h1>CSV-Datei hochladen</h1>
      
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={handleUpload}>Hochladen</button>

      {response && (
        <div>
          <h2>Ergebnisse</h2>
          <p><strong>Status:</strong> {response.status}</p>
          <p><strong>Verarbeitete Zeilen:</strong> {response.rows}</p>
          <p><strong>Durchschnittliche Verkäufe:</strong> {response.average_sales.toFixed(2)}</p>
          <p><strong>Standardabweichung:</strong> {response.std_sales.toFixed(2)}</p>

          {response.anomalies && response.anomalies.length > 0 ? (
            <div>
              <h3>Anomalien:</h3>
              <ul>
                {response.anomalies.map((anomaly, index) => (
                  <li key={index}>
                    <strong>Datum:</strong> {anomaly.date}, 
                    <strong> Verkäufe:</strong> {anomaly.sales}, 
                    <strong> Grund:</strong> {anomaly.reason}
                  </li>
                ))}
              </ul>
            </div>
          ) : (
            <p>Keine Anomalien gefunden.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
