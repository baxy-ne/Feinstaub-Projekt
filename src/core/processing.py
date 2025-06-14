import csv
import os
from datetime import datetime

def process_csv_data(folder):
    results = []
    for filename in os.listdir(folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder, filename)
            print(f"Processing file: {filename}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    
                    # Initialize variables for this file
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
                    
                    for row in reader:
                        try:
                            # Skip if sensor type is not sds011
                            if row.get('sensor_type', '').lower() != 'sds011':
                                continue
                                
                            # Handle empty values
                            p1 = row.get('P1', '0')
                            p2 = row.get('P2', '0')
                            
                            if p1.strip() and p2.strip():  # Only process if values are not empty
                                current_pollution_P1 = float(p1)
                                current_pollution_P2 = float(p2)
                                
                                # Update max and min values
                                max_p1 = max(max_p1, current_pollution_P1)
                                min_p1 = min(min_p1, current_pollution_P1)
                                max_p2 = max(max_p2, current_pollution_P2)
                                min_p2 = min(min_p2, current_pollution_P2)
                                
                                # Add to totals for average
                                total_p1 += current_pollution_P1
                                total_p2 += current_pollution_P2
                                count += 1
                                
                                # Store values for later use
                                pollution_values_p1.append(current_pollution_P1)
                                pollution_values_p2.append(current_pollution_P2)
                                timestamps.append(row.get('timestamp', ''))
                                
                        except (ValueError, KeyError) as e:
                            print(f"Warning: Skipping invalid row in {filename}: {e}")
                            continue
                    
                    if count > 0:  # Only process if we have valid data
                        # Calculate averages
                        avg_p1 = total_p1 / count
                        avg_p2 = total_p2 / count
                        
                        # Extract date from filename (assuming format: YYYY-MM-DD_sds011_sensor_XXXXX.csv)
                        date_str = filename.split('_')[0]
                        
                        result = {
                            'date': date_str,
                            'max_p1': max_p1,
                            'min_p1': min_p1,
                            'avg_p1': avg_p1,
                            'max_p2': max_p2,
                            'min_p2': min_p2,
                            'avg_p2': avg_p2,
                            'pollution_values_p1': pollution_values_p1,
                            'pollution_values_p2': pollution_values_p2,
                            'timestamps': timestamps
                        }
                        results.append(result)
                        
                        print(f"Saved data for sensor {filename.split('_')[3].split('.')[0]} on {date_str}")
                        print(f"Max P1: {max_p1:.2f}, Max P2: {max_p2:.2f}")
                        print(f"Min P1: {min_p1:.2f}, Min P2: {min_p2:.2f}")
                        print(f"Avg P1: {avg_p1:.2f}, Avg P2: {avg_p2:.2f}\n")
                        
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                continue
                
    return results

