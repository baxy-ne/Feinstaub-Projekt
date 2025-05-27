import csv
 
def process_csv_data(folder):
    max_temperature = float('-inf')
    min_temperature = float('inf')
    list_of_temperatures = []
    list_of_time = []
    list_of_dates = []
    all_temp = 0
 
    with open (folder, "r") as file:
        data = csv.DictReader(file, delimiter=";")
        i = 0
        for row in data:
            i += 1
            current_temperature = float(row["temperature"])
            list_of_temperatures.append(current_temperature)
            time = row["timestamp"].split("T")
            list_of_time.append(time[1])
            list_of_dates.append(time[0])
           
            if current_temperature > max_temperature:
                max_temperature = current_temperature
            if current_temperature < min_temperature:
                min_temperature = current_temperature
               
            all_temp += float(current_temperature)

        average_temperature = all_temp / i
        return [
            max_temperature,
            min_temperature,
            average_temperature,
            list_of_temperatures,
            list_of_time,
            list_of_dates
        ]
print(process_csv_data("2024-01-20_bme280_sensor_141.csv"))