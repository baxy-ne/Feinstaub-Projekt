import requests
import gzip
import os
import io


def datum_begin(datum):
    day = datum[0:1]
    month = datum[3:5]
    year = datum[6:]
    return day,month,year

def datum_end(datum):
    day = datum[0:1]
    month = datum[3:5]
    year = datum[6:]
    return day,month,year
   
MAIN_WEBSITE = "https://archive.sensor.community/"
DEFAULT_DOWNLOAD_FOLDER = "./downloads"

def days_in_month(year, month):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            return 29
        return 28
    return 0
 
def build_url(year, month, day, sensor_type, sensor_id):
    month = str(month).zfill(2)
    day = str(day).zfill(2)
    if year < 2023:
        return f"{MAIN_WEBSITE}{year}/{year}-{month}-{day}/{year}-{month}-{day}_{sensor_type}_sensor_{sensor_id}.csv.gz"
    else:
        return f"{MAIN_WEBSITE}{year}-{month}-{day}/{year}-{month}-{day}_{sensor_type}_sensor_{sensor_id}.csv"
 
def download_csv_files(year, month, sensor_type, sensor_id, folder):
    days = days_in_month(year, month)
    for day in range(1, days + 1):
        url = build_url(year, month, day, sensor_type, sensor_id)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                filename = url.split('/')[-1]
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
        except Exception as e:
            print(f"Error downloading {url}: {e}")