from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import csv
import io
import numpy as np  # Für Berechnungen wie Durchschnitt und Standardabweichung

# Initialisiere FastAPI-Anwendung
app = FastAPI()

# CORS-Middleware hinzufügen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Erlaube die URL des Frontends
    allow_credentials=True,
    allow_methods=["*"],  # Erlaube alle HTTP-Methoden
    allow_headers=["*"],  # Erlaube alle Header
)

# Datei-Upload-Endpunkt
@app.post("/upload_data/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Lies die Datei
        contents = await file.read()
        # CSV-Daten auslesen
        csv_file = io.StringIO(contents.decode())
        reader = csv.DictReader(csv_file)
        rows = list(reader)

        # Berechnungen und Anomalien
        sales = [float(row['sales']) for row in rows]  # Annahme: 'sales' ist der Name der Spalte mit Verkaufswerten
        avg_sales = np.mean(sales)
        std_sales = np.std(sales)

        # Erkennung von Anomalien
        anomalies = [
            {"date": row['date'], "sales": row['sales'], "reason": "Anomalie: Außerhalb 2 Std-Abw."}
            for row in rows if abs(float(row['sales']) - avg_sales) > 2 * std_sales
        ]

        # Erfolgreiche Antwort zurückgeben
        return JSONResponse(content={
            "status": "Daten hochgeladen",
            "rows": len(rows),
            "average_sales": avg_sales,
            "std_sales": std_sales,
            "anomalies": anomalies,
            "message": "Die Datei wurde erfolgreich verarbeitet!"
        }, status_code=200)

    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=422)

# Manuelle OPTIONS-Unterstützung für Preflight-Anfragen
@app.options("/upload_data/")
async def options_handler():
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
        status_code=200,
    )
