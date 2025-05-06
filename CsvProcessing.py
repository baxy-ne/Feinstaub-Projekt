import csv
 
def process_csv_data(folder):
    maxTemperature = float('-inf')
    minTemperature = float('inf')
    all_temp = 0
 
    with open (folder, "r") as file:
        data = csv.DictReader(file, delimiter=";")
 
        for row in data:
           
            current_temperature = float(row["temperature"])
           
           
            if current_temperature > maxTemperature:
                maxTemperature = current_temperature
            if current_temperature < minTemperature:
                minTemperature = current_temperature
               
            all_temp += float(current_temperature)


process_csv_data("2024-01-20_bme280_sensor_141.csv")