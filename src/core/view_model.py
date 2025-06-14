from src.download.downloader import download_csv_files
from src.core.processing import process_csv_data
from src.core.database import init_db, save_sensor_data, print_database_stats, get_date_range_data
import os

# Initialize database when module is imported
init_db()

def download_data(sensor_type, sensor_id, start_date, end_date, folder):
    print(f"\nDownloading data for sensor {sensor_id} from {start_date} to {end_date}")
    download_csv_files(start_date, end_date, sensor_type, sensor_id, folder)
    print_database_stats()

def process_data(folder):
    print(f"\nProcessing files in folder: {folder}")
    
    # Check if it's a file or directory
    if os.path.isfile(folder):
        # If it's a file, process just that file
        result = process_csv_data(os.path.dirname(folder))
    else:
        # If it's a directory, process all CSV files in it
        result = process_csv_data(folder)
    
    if result:
        for data in result:
            save_sensor_data(data)
    print_database_stats()
    return result