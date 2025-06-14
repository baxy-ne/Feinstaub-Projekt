from CSV_Download import download_csv_files
from CsvProcessing import process_csv_data
from database import init_db, save_sensor_data, print_database_stats
import os

# Initialize database when module is imported
init_db()

def download_data(start_date, end_date, sensor_type, sensor_id, folder):
    print(f"\nDownloading data for sensor {sensor_id} from {start_date} to {end_date}")
    download_csv_files(start_date, end_date, sensor_type, sensor_id, folder)
    print_database_stats()

def process_data(folder):
    print(f"\nProcessing files in folder: {folder}")
    results = []
    for filename in os.listdir(folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder, filename)
            print(f"\nProcessing file: {filename}")
            result = process_csv_data(file_path)
            if result:
                parts = filename.split('_')
                date = parts[0]
                sensor_id = parts[3].split('.')[0]
                save_sensor_data(sensor_id, 'SDS011', date, result)
                results.append(result)
    print_database_stats()
    return results