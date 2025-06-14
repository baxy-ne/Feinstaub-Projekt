import requests
import gzip
import os
import io
import datetime
from src.core.database import is_file_downloaded, mark_file_downloaded, get_date_range_data

MAIN_WEBSITE = "https://archive.sensor.community/"

def build_url(year, month, day, sensor_type, sensor_id):
    month = str(month).zfill(2)
    day = str(day).zfill(2)
    if year < 2023:
        return f"{MAIN_WEBSITE}{year}/{year}-{month}-{day}/{year}-{month}-{day}_{sensor_type}_sensor_{sensor_id}.csv.gz"
    else:
        return f"{MAIN_WEBSITE}{year}-{month}-{day}/{year}-{month}-{day}_{sensor_type}_sensor_{sensor_id}.csv"

def convert_string_to_date(date):
    day = date[0:2]
    month = date[3:5]
    year = date[6:]
    day = int(day)
    month = int(month)
    year = int(year)
    datum = datetime.date(year, month, day)
    return datum

def format_date_for_db(date):
    return date.strftime('%Y-%m-%d')

def download_csv_files(datum_begin: datetime.date, datum_end: datetime.date, sensor_type, sensor_id, folder):
    datum_begin = convert_string_to_date(datum_begin)
    datum_end = convert_string_to_date(datum_end)
    
    existing_dates = get_date_range_data(sensor_id, format_date_for_db(datum_begin), format_date_for_db(datum_end))
    print(f"Found {len(existing_dates)} existing data points in date range")
    
    current_date = datum_begin
    while current_date <= datum_end:
        current_date_str = format_date_for_db(current_date)
        
        if current_date_str in existing_dates:
            print(f"Skipping {current_date_str} - data already exists")
            current_date += datetime.timedelta(days=1)
            continue
            
        year = current_date.year
        month = current_date.month
        day = current_date.day
        url = build_url(year, month, day, sensor_type, sensor_id)
        filename = url.split('/')[-1]
        
        if is_file_downloaded(filename):
            print(f"Skipping already downloaded file: {filename}")
            current_date += datetime.timedelta(days=1)
            continue
            
        try:
            response = requests.get(url)
            if response.status_code == 200:
                filepath = os.path.join(folder, filename)
                if year < 2023:
                    filepath = filepath[:-3]
                    with gzip.open(io.BytesIO(response.content), 'rt') as gz_file:
                        with open(filepath, 'w', encoding='utf-8') as out_file:
                            out_file.write(gz_file.read())
                else:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                print(f"Downloaded: {filename}")
                mark_file_downloaded(filename)
        except Exception as e:
            print(f"Error downloading {url}: {e}")
        current_date += datetime.timedelta(days=1)
