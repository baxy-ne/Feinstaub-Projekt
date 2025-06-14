# Feinstaub-Projekt by Jannik Sauer, Onur Goekcek and William Gutschmidt

A Python application for downloading and processing air quality sensor data.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## Features

- Download air quality sensor data from sensor.community
- Process CSV files containing sensor data
- Store data in SQLite database
- View and analyze air quality measurements
- Support for sensor type sds011

## Project Structure

```
Feinstaub-Projekt/
├── data/
│   └── sensor_data.db
├── src/
│   ├── core/
│   │   ├── database.py
│   │   ├── processing.py
│   │   ├── consts.py
│   │   └── view_model.py
│   ├── download/
│   │   └── downloader.py
│   └── gui/
│       ├── gui.py
│       └── utils.py
├── main.py
└── requirements.txt
```

## Dependencies

- Python 3.x
- requests
- tkcalendar
- tkinter
