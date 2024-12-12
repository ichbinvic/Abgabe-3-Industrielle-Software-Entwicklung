import pandas as pd

def open_file(file_name):
    # Datei einlesen und direkt in ein Pandas DataFrame laden
    data = pd.read_csv(
        file_name,
        delimiter=';',  # Semikolon als Trennzeichen
        header=0        # Erste Zeile als Header verwenden
    )

    # Spalte "Date" ins amerikanische Zeitformat transformieren
    data['Date'] = pd.to_datetime(data['Date'], format='%d.%m.%Y', errors='coerce').dt.strftime('%m/%d/%Y')

    return data

# Datei einlesen
file_path = 'FinancialSample.csv'  # Pfad zur CSV-Datei
data = open_file(file_path)

# Die ersten 5 Zeilen jeder Spalte ausgeben
for column in data.columns:
    print(f"{column}: {data[column].head(5).tolist()} ...")
