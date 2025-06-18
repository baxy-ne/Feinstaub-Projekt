import requests
import gzip
import io
import datetime
from src.core.database import get_db_connection, get_date_range_data

def build_url(year, month, day, sensor_type, sensor_id):
    if year <= 2023:
        return f"https://archive.sensor.community/{year}/{year}-{month:02d}-{day:02d}/{year}-{month:02d}-{day:02d}_{sensor_type}_sensor_{sensor_id}.csv.gz"
    else:
        return f"https://archive.sensor.community/{year}-{month:02d}-{day:02d}/{year}-{month:02d}-{day:02d}_{sensor_type}_sensor_{sensor_id}.csv"

def convert_string_to_date(date_str):
    if isinstance(date_str, str):
        return datetime.datetime.strptime(date_str, '%d.%m.%Y').date()
    return date_str

def format_date_for_db(date):
    return date.strftime('%Y-%m-%d')

def download_csv_files(datum_begin: datetime.date, datum_end: datetime.date, sensor_type, sensor_id, folder):
    datum_begin = convert_string_to_date(datum_begin)
    datum_end = convert_string_to_date(datum_end)
    
    conn = get_db_connection()
    c = conn.cursor()
    
    downloaded_contents = []

    # Prüfe, welche Daten bereits für diese spezifische Sensor-ID existieren
    existing_dates = get_date_range_data(sensor_id, format_date_for_db(datum_begin), format_date_for_db(datum_end))
    existing_date_strings = [data['date'] for data in existing_dates]
    print(f"Found {len(existing_dates)} existing data points for sensor {sensor_id} in date range")
    
    current_date = datum_begin
    while current_date <= datum_end:
        current_date_str = format_date_for_db(current_date)
        
        if current_date_str in existing_date_strings:
            print(f"Skipping {current_date_str} - data already exists for sensor {sensor_id} in DB")
            current_date += datetime.timedelta(days=1)
            continue
            
        year = current_date.year
        month = current_date.month
        day = current_date.day
        url = build_url(year, month, day, sensor_type, sensor_id)
        filename = url.split('/')[-1]
            
        try:
            response = requests.get(url)
            if response.status_code == 200:
                if year <= 2023:
                    # Für Daten vor 2023: Entpacke die gz-Datei
                    csv_content = gzip.open(io.BytesIO(response.content), 'rt', encoding='utf-8').read()
                else:
                    # Für Daten ab 2023: Direkt als CSV lesen
                    csv_content = response.content.decode('utf-8')
                
                downloaded_contents.append((filename, csv_content))
                print(f"Downloaded content for: {filename}")

        except Exception as e:
            print(f"Error downloading {url}: {e}")
        current_date += datetime.timedelta(days=1)
        
    conn.close()
    return downloaded_contents
