import sqlite3
import os

def get_db_connection():
    db_dir = os.path.dirname('data/sensor_data.db')
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    return sqlite3.connect('data/sensor_data.db')

def init_db():
    """Initialisiert die Datenbank mit den notwendigen Tabellen"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Erstelle die Tabelle sensor_data, falls sie nicht existiert
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT NOT NULL,
            sensor_type TEXT NOT NULL,
            date TEXT NOT NULL,
            timestamp TEXT,
            max_p1 REAL,
            max_p2 REAL,
            min_p1 REAL,
            min_p2 REAL,
            avg_p1 REAL,
            avg_p2 REAL,
            location TEXT,
            lat REAL,
            lon REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(sensor_id, sensor_type, date)
        )
    ''')
    
    # Erstelle die Tabelle downloaded_files, falls sie nicht existiert
    c.execute('''
        CREATE TABLE IF NOT EXISTS downloaded_files (
            filename TEXT PRIMARY KEY,
            downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized")

def is_file_downloaded(conn, cursor, filename):
    """Prüft, ob eine Datei bereits heruntergeladen wurde.
    Akzeptiert conn und cursor als Argumente.
    """
    cursor.execute('SELECT 1 FROM downloaded_files WHERE filename = ?', (filename,))
    result = cursor.fetchone() is not None
    if result:
        print(f"File already in database: {filename}")
    return result

def mark_file_downloaded(conn, cursor, filename):
    """Markiert eine Datei als heruntergeladen.
    Akzeptiert conn und cursor als Argumente.
    """
    cursor.execute('INSERT OR IGNORE INTO downloaded_files (filename) VALUES (?)', (filename,))
    conn.commit()
    print(f"Marked as downloaded: {filename}")

def save_sensor_data(conn, cursor, sensor_id, sensor_type, date, stats):
    """Speichert Sensordaten in der Datenbank.
    Akzeptiert conn und cursor als Argumente.
    """
    # Debug-Ausgabe vor dem Speichern
    print("\nSpeichere Daten in der Datenbank:")
    print(f"Location: {stats.get('location', 'Nicht gefunden')}")
    print(f"Lat: {stats.get('lat', 'Nicht gefunden')}")
    print(f"Lon: {stats.get('lon', 'Nicht gefunden')}")
    
    cursor.execute('''
        INSERT OR IGNORE INTO sensor_data 
        (sensor_id, sensor_type, date, timestamp, max_p1, max_p2, min_p1, min_p2, avg_p1, avg_p2, location, lat, lon)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        sensor_id,
        sensor_type,
        date,
        stats.get('timestamp', ''),
        stats['max_pollution_1'],
        stats['max_pollution_2'],
        stats['min_pollution_1'],
        stats['min_pollution_2'],
        stats['average_P1'],
        stats['average_P2'],
        stats.get('location', ''),
        stats.get('lat'),
        stats.get('lon')
    ))
    
    # conn.commit() wird jetzt von der aufrufenden Funktion gehandhabt, die die Transaktion verwaltet
    # Nur die Debug-Ausgabe anpassen, um Ignorieren zu berücksichtigen
    if cursor.rowcount == 0:
        print(f"Skipping data for sensor {sensor_id} on {date}: Already exists.")
    else:
        print(f"Saved data for sensor {sensor_id} on {date}")
    print(f"Max P1: {stats['max_pollution_1']:.2f}, Max P2: {stats['max_pollution_2']:.2f}")
    print(f"Min P1: {stats['min_pollution_1']:.2f}, Min P2: {stats['min_pollution_2']:.2f}")
    print(f"Avg P1: {stats['average_P1']:.2f}, Avg P2: {stats['average_P2']:.2f}")

def get_sensor_data(sensor_id, date):
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''
        SELECT * FROM sensor_data 
        WHERE sensor_id = ? AND date = ?
    ''', (sensor_id, date))
    
    result = c.fetchone()
    if result:
        print(f"Found existing data for sensor {sensor_id} on {date}")
    conn.close()
    return result

def get_date_range_data(sensor_id, start_date, end_date):
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''
        SELECT * FROM sensor_data 
        WHERE sensor_id = ? AND date BETWEEN ? AND ?
        ORDER BY date
    ''', (sensor_id, start_date, end_date))
    
    columns = [description[0] for description in c.description]
    data = [dict(zip(columns, row)) for row in c.fetchall()]
    
    # Debug-Ausgabe
    if data:
        print("\nGeladene Daten aus der Datenbank:")
        print(f"Anzahl der Datensätze: {len(data)}")
        print("Erster Datensatz:")
        for key, value in data[0].items():
            print(f"{key}: {value}")
    
    conn.close()
    return data

def print_database_stats():
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM sensor_data')
    sensor_count = c.fetchone()[0]
    print(f"\nTotal sensor data entries: {sensor_count}")
    
    c.execute('SELECT COUNT(*) FROM downloaded_files')
    file_count = c.fetchone()[0]
    print(f"Total downloaded files: {file_count}")
    
    c.execute('SELECT sensor_id, COUNT(*) FROM sensor_data GROUP BY sensor_id')
    sensor_stats = c.fetchall()
    print("\nData per sensor:")
    for sensor_id, count in sensor_stats:
        print(f"Sensor {sensor_id}: {count} entries")
    
    conn.close()

def load_sensor_data(sensor_id, sensor_type, date):
    conn = get_db_connection()
    c = conn.cursor()
    
    print(f"\nLade Daten aus der Datenbank für:")
    print(f"Sensor ID: {sensor_id}")
    print(f"Sensor Type: {sensor_type}")
    print(f"Datum: {date}")
    
    # Debug: Zeige alle verfügbaren Daten für diesen Sensor
    c.execute('''
        SELECT * FROM sensor_data 
        WHERE sensor_id = ? AND sensor_type = ?
    ''', (sensor_id, sensor_type))
    
    all_rows = c.fetchall()
    print("\nAlle verfügbaren Daten für diesen Sensor:")
    for row in all_rows:
        print(f"Date: {row[3]}, Location: {row[10]}, Lat: {row[11]}, Lon: {row[12]}")
    
    # Lade die spezifischen Daten für das angegebene Datum
    c.execute('''
        SELECT * FROM sensor_data 
        WHERE sensor_id = ? AND sensor_type = ? AND date = ?
    ''', (sensor_id, sensor_type, date))
    
    row = c.fetchone()
    conn.close()
    
    if row:
        print("\nGeladene Daten aus der Datenbank:")
        print(f"Location: {row[10] if row[10] else 'Nicht gefunden'}")
        print(f"Lat: {row[11] if row[11] else 'Nicht gefunden'}")
        print(f"Lon: {row[12] if row[12] else 'Nicht gefunden'}")
        
        data = {
            'timestamp': row[3],
            'max_pollution_1': row[4],
            'max_pollution_2': row[5],
            'min_pollution_1': row[6],
            'min_pollution_2': row[7],
            'average_P1': row[8],
            'average_P2': row[9],
            'location': row[10] if row[10] else '',
            'lat': row[11],
            'lon': row[12]
        }
        print("\nZurückgegebene Daten:")
        print(f"Location: {data['location']}")
        print(f"Lat: {data['lat']}")
        print(f"Lon: {data['lon']}")
        return data
    print("Keine Daten gefunden!")
    return None 