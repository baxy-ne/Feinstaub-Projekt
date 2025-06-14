import csv
 
def process_csv_data(folder):
    with open(folder, "r") as file:
        data = csv.DictReader(file, delimiter=";")
        first_row = next(data)
        sensor_type = first_row.get('sensor_type', '')
        
        if sensor_type != 'SDS011':
            print(f"Skipping non-SDS011 file: {folder}")
            return None
            
        file.seek(0)
        next(data)  
        
        max_pollution_p1 = float('-inf')
        max_pollution_p2 = float('-inf')
        min_pullution_p1 = float('inf')
        min_pullution_p2 = float('inf')
        all_pollution_p1 = 0
        all_pollution_p2 = 0
        list_of_pollution_p1 = []
        list_of_pollution_p2 = []
        list_of_time = []
        list_of_dates = []
        
        i = 0
        for row in data:
            i += 1
            current_pollution_P1 = float(row["P1"])
            current_pollution_P2 = float(row["P2"])
            list_of_pollution_p1.append(current_pollution_P1)
            list_of_pollution_p2.append(current_pollution_P2)
            time = row["timestamp"].split("T")
            list_of_time.append(time[1])
            list_of_dates.append(time[0])
           
            if current_pollution_P1 > max_pollution_p1:
                max_pollution_p1 = current_pollution_P1
            if current_pollution_P1 < min_pullution_p1:
                min_pullution_p1 = current_pollution_P1

            if current_pollution_P2 > max_pollution_p2:
                max_pollution_p2 = current_pollution_P2
            if current_pollution_P2 < min_pullution_p2:
                min_pullution_p2 = current_pollution_P2
               
            all_pollution_p1 += float(current_pollution_P1)
            all_pollution_p2 += float(current_pollution_P2)

        average_P1 = all_pollution_p1 / i if i > 0 else 0
        average_P2 = all_pollution_p2 / i if i > 0 else 0
        
        return {
            "max_pollution_1": max_pollution_p1,
            "max_pollution_2": max_pollution_p2,
            "min_pollution_1": min_pullution_p1,
            "min_pollution_2": min_pullution_p2,
            "average_P1": average_P1,
            "average_P2": average_P2,
            "all_pollutions_1": list_of_pollution_p1,
            "all_pollutions_2": list_of_pollution_p2,
        }

