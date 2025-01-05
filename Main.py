import pandas as pd
import numpy as np
from scipy.signal import argrelextrema


# Funktion zum Anpassen der Discounts-Werte
def adjust_discount(value):
    # Falls der Wert "$- " ist, wird er als "Low" gewertet
    if value.strip() == "$-":
        return "Low"
    # Entferne alles außer Zahlen und Punkten und versuche, den Wert als Zahl zu interpretieren
    value = value.replace('$', '').replace(',', '')  # Entferne Dollarzeichen und Kommas
    try:
        value = float(value)
    except ValueError:
        return value  # Falls der Wert nicht als Zahl interpretiert werden kann, gib ihn unverändert zurück

    # Bedingungen zur Kategorisierung des Discounts
    if value <= 200:
        return 'Low'
    elif 200 < value < 2000:
        return 'Medium'
    elif value >= 2000:
        return 'High'
    return value  # Rückgabe des ursprünglichen Werts, falls kein Kriterium zutrifft


def open_file(file_name):
    # Datei einlesen und direkt in ein Pandas DataFrame laden
    data = pd.read_csv(
        file_name,
        delimiter=';',  # Semikolon als Trennzeichen
        header=0,  # Erste Zeile als Header verwenden
    )

    # Spaltennamen bereinigen, um führende/trailing Leerzeichen zu entfernen
    data.columns = data.columns.str.strip()

    # Spalte "Discounts" anpassen
    data['Discounts'] = data['Discounts'].apply(adjust_discount)

    # Spalte "Date" ins amerikanische Zeitformat transformieren
    data['Date'] = pd.to_datetime(data['Date'], format='%d.%m.%Y', errors='coerce').dt.strftime('%m/%d/%Y')

    return data


# Aufgabe 1
# Datei einlesen
file_path = 'FinancialSample.csv'  # Pfad zur CSV-Datei
data = open_file(file_path)
print("\nAufgabe 1:")
# Die ersten 5 Zeilen jeder Spalte ausgeben
for column in data.columns:
    print(f"{column}: {data[column].head(10).tolist()} ...")

# Aufgabe 3
# Neues DataFrame mit den gewünschten Spalten erstellen
selected_columns = ["Product", "Profit", "COGS", "Sales"]
filtered_data = data[selected_columns]

# Die ersten 5 Einträge des neuen DataFrames ausgeben
print("\nAufgabe 3:")
print(filtered_data.head(5).to_string(index=False))

# Spalten "Month Number", "Month Name" und "Year" zu einem kombinierten Datum verbinden
if all(col in data.columns for col in ["Month Number", "Month Name", "Year"]):
    # Kombiniertes Datum im gewünschten Format erstellen
    data['Combined Date'] = data['Month Name'].str.strip() + '/' + \
                            data['Month Number'].astype(str).str.zfill(2) + '/01/' + \
                            data['Year'].astype(str)

    # Die ersten 5 Einträge des neuen DataFrames ausgeben
    print("\nAufgabe 4:")
    print(data['Combined Date'].head(10).tolist())

# Aufgabe 5: Die 10 größten lokalen Maxima in der Spalte "Sales" finden

data['Sales'] = data['Sales'].str.replace('[^0-9.]', '', regex=True)  # Entferne alles außer Zahlen und Punkte
data['Sales'] = pd.to_numeric(data['Sales'], errors='coerce')  # Konvertiere in float

# Indizes der lokalen Maxima finden
local_maxima_indices = argrelextrema(data['Sales'].values, np.greater, order=1)[0]

# Lokale Maxima extrahieren
local_maxima = data.iloc[local_maxima_indices]

# Die 10 größten lokalen Maxima auswählen
top_10_maxima = local_maxima.nlargest(10, 'Sales')

print("\nAufgabe 5: \nMaxima in der Spalte 'Sales':")
print(top_10_maxima[['Sales']])

# Aufgabe 6: Erzeuge ein neues DataFrame mit jeder X-ten Zeile
X = 5  # Gruppennummer, z.B. jede 3. Zeile
sampled_data = data.iloc[::X]

print("\nAufgabe 6: Jede 5-te Zeile des DataFrames:")
print(sampled_data.head(10).to_string(index=False))
