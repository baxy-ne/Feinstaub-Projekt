from src.download.downloader import download_csv_files
from src.core.processing import process_csv_data
from src.core.database import init_db, save_sensor_data, print_database_stats, get_date_range_data
import os

init_db()

def download_data(sensor_type, sensor_id, start_date, end_date, folder):
    print(f"\nDownloading data for sensor {sensor_id} from {start_date} to {end_date}")
    download_csv_files(start_date, end_date, sensor_type, sensor_id, folder)
    print_database_stats()

def process_data(folder):
    print(f"\nProcessing files in folder: {folder}")
    
    if os.path.isfile(folder):
        result = process_csv_data(os.path.dirname(folder))
    else:
        result = process_csv_data(folder)
    
    if result:
        for data in result:
            stats = {
                'max_pollution_1': data['max_p1'],
                'max_pollution_2': data['max_p2'],
                'min_pollution_1': data['min_p1'],
                'min_pollution_2': data['min_p2'],
                'average_P1': data['avg_p1'],
                'average_P2': data['avg_p2']
            }
            save_sensor_data(data['sensor_id'], data['sensor_type'], data['date'], stats)
    print_database_stats()
    return result