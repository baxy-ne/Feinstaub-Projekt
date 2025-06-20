import csv
import os
import io
import pandas as pd
from src.core.database import mark_file_downloaded
from datetime import datetime

def process_csv_data(conn, c, filename, csv_content):
    try:
        df = pd.read_csv(io.StringIO(csv_content), sep=';')
        
        date_str = filename.split('_')[0]
        
        sensor_id = str(df['sensor_id'].iloc[0])
        sensor_type = str(df['sensor_type'].iloc[0])
        
        location = str(df['location'].iloc[0]) if 'location' in df.columns and not pd.isna(df['location'].iloc[0]) else None
        lat = float(df['lat'].iloc[0]) if 'lat' in df.columns and not pd.isna(df['lat'].iloc[0]) else None
        lon = float(df['lon'].iloc[0]) if 'lon' in df.columns and not pd.isna(df['lon'].iloc[0]) else None
        
        stats = {
            'max_pollution_1': df['P1'].max() if 'P1' in df.columns else None,
            'max_pollution_2': df['P2'].max() if 'P2' in df.columns else None,
            'min_pollution_1': df['P1'].min() if 'P1' in df.columns else None,
            'min_pollution_2': df['P2'].min() if 'P2' in df.columns else None,
            'average_P1': df['P1'].mean() if 'P1' in df.columns else None,
            'average_P2': df['P2'].mean() if 'P2' in df.columns else None,
            'location': location,
            'lat': lat,
            'lon': lon,
            'timestamp': df['timestamp'].iloc[0] if 'timestamp' in df.columns else None
        }
        
        c.execute('''
            INSERT OR IGNORE INTO sensor_data 
            (sensor_id, sensor_type, date, timestamp, max_pollution_1, max_pollution_2, min_pollution_1, min_pollution_2, average_P1, average_P2, location, lat, lon)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            sensor_id,
            sensor_type,
            date_str,
            stats['timestamp'],
            stats['max_pollution_1'],
            stats['max_pollution_2'],
            stats['min_pollution_1'],
            stats['min_pollution_2'],
            stats['average_P1'],
            stats['average_P2'],
            stats['location'],
            stats['lat'],
            stats['lon']
        ))
        
        conn.commit()
        mark_file_downloaded(conn, c, filename)

    except Exception as e:
        conn.rollback()

