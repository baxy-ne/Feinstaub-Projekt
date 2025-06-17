# Feinstaub-Projekt

Ein Python-Programm zur Analyse von Feinstaubdaten von sds011-Sensoren.

## Funktionen

- Download von CSV-Dateien von [sensor.community](https://archive.sensor.community/)
- Automatische Speicherung der Daten in einer SQLite-Datenbank
- Analyse der Feinstaubdaten (PM2.5 und PM10)
- Grafische Darstellung der Messwerte
- Export der Diagramme als PDF oder PNG

## Installation

1. Stellen Sie sicher, dass Python 3.x installiert ist
2. Klonen Sie das Repository:
```bash
git clone [Repository-URL]
cd FeinstaubProjekt
```

3. Installieren Sie die erforderlichen Abhängigkeiten:
```bash
pip install -r requirements.txt
```

## Verwendung

1. Starten Sie das Programm:
```bash
python main.py
```

2. In der grafischen Benutzeroberfläche:
   - Wählen Sie den gewünschten Zeitraum
   - Geben Sie die Sensor-ID ein
   - Wählen Sie einen Zielordner für die heruntergeladenen Dateien
   - Klicken Sie auf "Download Data" um die Daten herunterzuladen
   - Klicken Sie auf "Save Data to DB" um die Daten in die Datenbank zu speichern
   - Klicken Sie auf "show diagram" um die Daten grafisch darzustellen

3. Im Diagramm-Fenster:
   - Die Daten werden als zwei Graphen dargestellt (PM10 und PM2.5)
   - Klicken Sie auf "Speichern" um das Diagramm als PDF oder PNG zu exportieren
   - Klicken Sie auf "Schließen" um das Diagramm-Fenster zu schließen

## Datenbankstruktur

Die SQLite-Datenbank speichert folgende Informationen:
- Datum und Uhrzeit der Messung
- Sensor-ID
- PM2.5-Wert (in μg/m³)
- PM10-Wert (in μg/m³)
- Maximale, minimale und durchschnittliche Werte pro Tag

## Technische Details

- Programmiersprache: Python
- GUI: Tkinter
- Datenbank: SQLite
- Grafische Darstellung: Matplotlib
- Datenverarbeitung: Pandas

## Projektstruktur

```
Feinstaub-Projekt/
├── data/
│   └── sensor_data.db
├── src/
│   ├── core/
│   │   ├── database.py
│   │   ├── processing.py
│   │   ├── consts.py
│   │   ├── view_model.py
│   │   └── plotting.py
│   ├── download/
│   │   └── downloader.py
│   └── gui/
│       ├── gui.py
│       └── utils.py
├── main.py
├── requirements.txt
└── README.md
```

## Fehlerbehebung

Falls Probleme auftreten:
1. Überprüfen Sie die Internetverbindung
2. Stellen Sie sicher, dass alle Abhängigkeiten installiert sind
3. Überprüfen Sie, ob der gewählte Zeitraum gültig ist
4. Stellen Sie sicher, dass der Zielordner existiert und beschreibbar ist

## Lizenz

Dieses Projekt ist Open Source und unter der MIT-Lizenz verfügbar.
