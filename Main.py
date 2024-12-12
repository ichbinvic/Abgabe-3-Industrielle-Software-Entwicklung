import pandas as pd

def open_file(file_name):
    # Datei einlesen und direkt in ein Pandas DataFrame laden
    data = pd.read_csv(
        file_name,
        delimiter=';',  # Semikolon als Trennzeichen
        header=0        # Erste Zeile als Header verwenden
    )

    # Spaltennamen bereinigen, um führende/trailing Leerzeichen zu entfernen
    data.columns = data.columns.str.strip()

    # Spalte "Date" ins amerikanische Zeitformat transformieren
    data['Date'] = pd.to_datetime(data['Date'], format='%d.%m.%Y', errors='coerce').dt.strftime('%m/%d/%Y')

    return data

# Datei einlesen
file_path = 'FinancialSample.csv'  # Pfad zur CSV-Datei
data = open_file(file_path)

# Die ersten 5 Zeilen jeder Spalte ausgeben
for column in data.columns:
    print(f"{column}: {data[column].head(5).tolist()} ...")

# Neues DataFrame mit den gewünschten Spalten erstellen
selected_columns = ["Product", "Profit", "COGS", "Sales"]
filtered_data = data[selected_columns]

# Die ersten 5 Einträge des neuen DataFrames ausgeben
print("\nFiltered DataFrame:")
print(filtered_data.head(5))

# Spalten "Month Number", "Month Name" und "Year" zu einem kombinierten Datum verbinden
if all(col in data.columns for col in ["Month Number", "Month Name", "Year"]):
    data['Combined Date'] = pd.to_datetime(
        data['Year'].astype(str) + '-' + data['Month Number'].astype(str),
        format='%Y-%m',
        errors='coerce'
    ).dt.strftime('%m/%Y')

    # DataFrame auf die kombinierte Spalte reduzieren
    data = data[['Combined Date']]

    # Die ersten 5 Einträge des neuen DataFrames ausgeben
    print("\nCombined Date DataFrame:")
    print(data['Combined Date'].head(5).tolist())
