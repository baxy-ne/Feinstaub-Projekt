from src.download.downloader import download_csv_files
from src.core.processing import process_csv_data
from src.core.database import init_db, get_db_connection, save_sensor_data, print_database_stats, get_date_range_data
import os

def download_data(sensor_type, sensor_id, start_date, end_date):
    print(f"\nDownloading data for sensor {sensor_id} from {start_date} to {end_date}")
    conn = get_db_connection()

    try:
        downloaded_contents = download_csv_files(start_date, end_date, sensor_type, sensor_id, None)

        c = conn.cursor()
        for filename, csv_content in downloaded_contents:
            process_csv_data(conn, c, filename, csv_content)

        conn.close()
        print_database_stats()
        return True
    except Exception as e:
        if conn:
            conn.close()
        print(f"Error in download_data: {e}")
        return False