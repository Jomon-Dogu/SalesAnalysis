from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import numpy as np
import csv
import io
import logging
from fastapi.middleware.cors import CORSMiddleware

# Logging-Konfiguration
logging.basicConfig(level=logging.DEBUG)

# FastAPI-Anwendung erstellen
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Passe hier die Frontend-Domain an
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/upload_data/")
async def upload_file(file: UploadFile = File(...)):
    try:
        logging.debug("Datei empfangen: %s", file.filename)

        # Datei lesen
        contents = await file.read()
        csv_file = io.StringIO(contents.decode())
        reader = csv.DictReader(csv_file)
        rows = list(reader)

        # Initialisiere Ergebnisse
        numerical_columns = {}
        anomalies = []

        # Durchlaufe alle Spalten
        for column in reader.fieldnames:
            try:
                # Sammle numerische Werte
                values = [
                    float(row[column].replace(',', '.'))
                    for row in rows if row[column].strip()
                ]

                # Nur Berechnung durchführen, wenn Werte vorhanden sind
                if values:
                    mean = np.mean(values)
                    std = np.std(values)
                else:
                    mean = None
                    std = None

                numerical_columns[column] = {
                    "mean": mean,
                    "std": std
                }

                # Finde Anomalien
                column_anomalies = [
                    {
                        "row": i,
                        "value": row[column],
                        "reason": f"Anomalie: Wert {row[column]} außerhalb von 2 Std-Abw."
                    }
                    for i, row in enumerate(rows)
                    if row[column].strip() and abs(float(row[column].replace(',', '.')) - mean) > 2 * std
                ] if mean is not None and std is not None else []

                anomalies.extend(column_anomalies)

            except ValueError:
                logging.warning(f"Spalte '{column}' enthält nicht-konvertierbare Werte.")
                continue

        return JSONResponse(content={
            "status": "Daten hochgeladen",
            "rows": len(rows),
            "numerical_columns": numerical_columns,
            "anomalies": anomalies
        }, status_code=200)

    except Exception as e:
        logging.error("Fehler: %s", str(e))
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=422)

# Starte die Anwendung (Nur für direkten Start, nicht in Produktion verwenden)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
