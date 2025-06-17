import csv
import os

def process_csv_data(folder):
    results = []
    for filename in os.listdir(folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder, filename)
            print(f"\nVerarbeite Datei: {filename}")
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter=';')
                    
                    # Debug: Zeige die verfügbaren Spalten
                    print("Verfügbare Spalten in der CSV:")
                    print(reader.fieldnames)

                    max_p1 = float('-inf')
                    min_p1 = float('inf')
                    max_p2 = float('-inf')
                    min_p2 = float('inf')
                    total_p1 = 0
                    total_p2 = 0
                    count = 0
                    pollution_values_p1 = []
                    pollution_values_p2 = []
                    timestamps = []
                    location = None
                    lat = None
                    lon = None

                    for row in reader:
                        try:
                            # Debug: Zeige die ersten paar Zeilen
                            if count < 3:
                                print("\nBeispiel-Zeile aus CSV:")
                                for key, value in row.items():
                                    print(f"{key}: {value}")

                            if row.get('sensor_type', '').lower() != 'sds011':
                                print(f"  Skipping row: sensor_type is '{row.get('sensor_type', '')}'")
                                continue
                                
                            p1_str = row.get('P1', '').strip()
                            p2_str = row.get('P2', '').strip()

                            if not p1_str or not p2_str:
                                print(f"  Skipping row: P1='{p1_str}', P2='{p2_str}' (empty)")
                                continue

                            current_pollution_P1 = float(p1_str)
                            current_pollution_P2 = float(p2_str)
                                
                            max_p1 = max(max_p1, current_pollution_P1)
                            min_p1 = min(min_p1, current_pollution_P1)
                            max_p2 = max(max_p2, current_pollution_P2)
                            min_p2 = min(min_p2, current_pollution_P2)
                                
                            total_p1 += current_pollution_P1
                            total_p2 += current_pollution_P2
                            count += 1
                                
                            pollution_values_p1.append(current_pollution_P1)
                            pollution_values_p2.append(current_pollution_P2)
                            timestamps.append(row.get('timestamp', ''))
                            
                            # Speichere Standortinformationen, wenn verfügbar
                            if not location and row.get('location'):
                                location = row.get('location')
                                print(f"Gefundene Location: {location}")
                            if not lat and row.get('lat'):
                                try:
                                    lat = float(row.get('lat'))
                                    print(f"Gefundene Latitude: {lat}")
                                except (ValueError, TypeError):
                                    lat = None
                            if not lon and row.get('lon'):
                                try:
                                    lon = float(row.get('lon'))
                                    print(f"Gefundene Longitude: {lon}")
                                except (ValueError, TypeError):
                                    lon = None
                                
                        except (ValueError, KeyError) as e:
                            print(f"  Warning: Skipping invalid row in {filename}: {e}")
                            continue
                    
                    if count > 0:
                        avg_p1 = total_p1 / count
                        avg_p2 = total_p2 / count
                        
                        parts = filename.split('_')
                        date_str = parts[0]
                        sensor_type = parts[1] if len(parts) > 2 else 'unknown'
                        sensor_id = parts[3].split('.')[0] if len(parts) > 3 else 'unknown'
                        
                        # Debug-Ausgabe für Standortinformationen
                        print(f"\nZusammenfassung für Sensor {sensor_id}:")
                        print(f"Location: {location}")
                        print(f"Lat: {lat}")
                        print(f"Lon: {lon}")
                        
                        result = {
                            'date': date_str,
                            'sensor_type': sensor_type,
                            'sensor_id': sensor_id,
                            'max_p1': max_p1,
                            'min_p1': min_p1,
                            'avg_p1': avg_p1,
                            'max_p2': max_p2,
                            'min_p2': min_p2,
                            'avg_p2': avg_p2,
                            'pollution_values_p1': pollution_values_p1,
                            'pollution_values_p2': pollution_values_p2,
                            'timestamps': timestamps,
                            'location': location,
                            'lat': lat,
                            'lon': lon
                        }
                        results.append(result)
                        
                        print(f"Saved data for sensor {sensor_id} on {date_str}")
                        print(f"Max P1: {max_p1:.2f}, Max P2: {max_p2:.2f}")
                        print(f"Min P1: {min_p1:.2f}, Min P2: {min_p2:.2f}")
                        print(f"Avg P1: {avg_p1:.2f}, Avg P2: {avg_p2:.2f}\n")
                    else:
                        print(f"  No valid data found in {filename}")
                        
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                continue
                
    return results

