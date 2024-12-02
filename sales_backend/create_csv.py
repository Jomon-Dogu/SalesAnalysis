import pandas as pd

# Beispiel-Daten
data = {
    "product_category": ["Electronics", "Clothing", "Electronics", "Groceries", "Clothing"],
    "sales": [1000, 500, 1900, 300, 700]
}

# DataFrame erstellen
df = pd.DataFrame(data)

# CSV-Datei speichern
df.to_csv("/home/wolff/git-repository/SalesAnalysis/azure_datalake/sales_data.csv", index=False)

print("Beispiel-CSV-Datei wurde erstellt.")
