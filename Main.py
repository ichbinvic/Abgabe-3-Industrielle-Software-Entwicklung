import pandas as pd

# Datei einlesen
file_path = 'FinancialSample.csv'  # Pfad zur CSV-Datei
data = pd.read_csv(
    file_path,
    delimiter=';',  # Semikolon als Trennzeichen
    decimal=',',    # Kommas als Dezimaltrennzeichen
    thousands='.'   # Punkte als Tausendertrennzeichen
)

# Die letzten 10 Elemente ausgeben
print(data.tail(10))

data['Date'] = pd.to_datetime(data['Date'], format='%d.%m.%Y').dt.strftime('%m/%d/%Y')
