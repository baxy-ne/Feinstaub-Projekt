import sqlite3
from datetime import datetime
import os

def get_db_connection():
    db_dir = os.path.dirname('data/sensor_data.db')
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    return sqlite3.connect('data/sensor_data.db')

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT,
            sensor_type TEXT,
            date TEXT,
            max_p1 REAL,
            max_p2 REAL,
            min_p1 REAL,
            min_p2 REAL,
            avg_p1 REAL,
            avg_p2 REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS downloaded_files (
            filename TEXT PRIMARY KEY,
            downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized")

def is_file_downloaded(filename):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT 1 FROM downloaded_files WHERE filename = ?', (filename,))
    result = c.fetchone() is not None
    if result:
        print(f"File already in database: {filename}")
    conn.close()
    return result

def mark_file_downloaded(filename):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO downloaded_files (filename) VALUES (?)', (filename,))
    conn.commit()
    conn.close()
    print(f"Marked as downloaded: {filename}")

def save_sensor_data(sensor_id, sensor_type, date, stats):
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO sensor_data 
        (sensor_id, sensor_type, date, max_p1, max_p2, min_p1, min_p2, avg_p1, avg_p2)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        sensor_id,
        sensor_type,
        date,
        stats['max_pollution_1'],
        stats['max_pollution_2'],
        stats['min_pollution_1'],
        stats['min_pollution_2'],
        stats['average_P1'],
        stats['average_P2']
    ))
    
    conn.commit()
    conn.close()
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
        SELECT date FROM sensor_data 
        WHERE sensor_id = ? AND date BETWEEN ? AND ?
        ORDER BY date
    ''', (sensor_id, start_date, end_date))
    
    existing_dates = [row[0] for row in c.fetchall()]
    conn.close()
    return existing_dates

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