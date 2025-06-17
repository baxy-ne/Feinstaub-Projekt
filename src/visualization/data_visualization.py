import matplotlib.pyplot as plt

class DataVisualization:
    def plot_data(self, sensor_id, sensor_type, date):
        """Plottet die Daten für einen bestimmten Sensor und Tag"""
        print(f"\nStarte plot_data für:")
        print(f"Sensor ID: {sensor_id}")
        print(f"Sensor Type: {sensor_type}")
        print(f"Datum: {date}")
        
        data = self.db.load_sensor_data(sensor_id, sensor_type, date)
        if not data:
            print(f"Keine Daten gefunden für Sensor {sensor_id} am {date}")
            return

        print("\nGeladene Daten für Plot:")
        print(f"Location: {data.get('location', 'Nicht gefunden')}")
        print(f"Lat: {data.get('lat', 'Nicht gefunden')}")
        print(f"Lon: {data.get('lon', 'Nicht gefunden')}")

        location_parts = []
        if data.get('location'):
            location_parts.append(f"Standort: {data['location']}")
        if data.get('lat') is not None and data.get('lon') is not None:
            location_parts.append(f"Lat: {data['lat']:.2f}, Lon: {data['lon']:.2f}")

        location_line = ""
        if location_parts:
            if len(location_parts) == 2:
                location_line = f"{location_parts[0]} ({location_parts[1]})"
            else:
                location_line = location_parts[0]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

        full_title = f'Sensor {sensor_id} Feinstaubdaten\nDatum: {date}'
        if location_line:
            full_title += f'\n{location_line}'
        
        fig.suptitle(full_title, fontsize=10, x=0.00, ha='left', y=1.00)

        ax1.plot([data['max_pollution_1']], [0], 'ro', label='Maximum')
        ax1.plot([data['min_pollution_1']], [0], 'bo', label='Minimum')
        ax1.plot([data['average_P1']], [0], 'go', label='Durchschnitt')
        ax1.set_title('')
        ax1.set_ylabel('µg/m³', fontsize=8)
        ax1.tick_params(axis='both', which='major', labelsize=8)
        ax1.legend(fontsize=7)
        ax1.grid(True)

        ax2.plot([data['max_pollution_2']], [0], 'ro', label='Maximum')
        ax2.plot([data['min_pollution_2']], [0], 'bo', label='Minimum')
        ax2.plot([data['average_P2']], [0], 'go', label='Durchschnitt')
        ax2.set_title('')
        ax2.set_ylabel('µg/m³', fontsize=8)
        ax2.tick_params(axis='both', which='major', labelsize=8)
        ax2.legend(fontsize=7)
        ax2.grid(True)

        plt.tight_layout(rect=[0, 0, 1, 0.90])
        print("\nPlot erstellt und zurückgegeben")
        return fig 