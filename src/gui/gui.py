import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from tkcalendar import DateEntry
from datetime import date, timedelta
from src.core.view_model import download_data
from src.core.consts import CONST_NOT_ALL_FIELDS_FILLED, sensor_type_list
from src.gui.utils import center_window
from src.core.plotting import plot_sensor_data
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.core.database import get_date_range_data, format_date_for_db

class SensorDataGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI concept")
        self.root.geometry("1280x1024")
        center_window(self.root)
        
        # Bindet das Schließen des Fensters an die quit_app Methode
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        
        self.target_folder_var = tk.StringVar()
        
        # Date Range
        ttk.Label(self.root, text="Date range").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        # Setze maxdate auf vorgestern für Startdatum und gestern für Enddatum
        yesterday = date.today() - timedelta(days=1)
        day_before_yesterday = date.today() - timedelta(days=2)
        
        self.start_date = DateEntry(
            self.root,
            date_pattern='dd.MM.yyyy',
            state='readonly',
            maxdate=day_before_yesterday
        )
        self.start_date.grid(row=0, column=1, padx=5)
        
        self.end_date = DateEntry(
            self.root,
            date_pattern='dd.MM.yyyy',
            state='readonly',
            mindate=self.start_date.get_date(),
            maxdate=yesterday
        )
        self.end_date.grid(row=0, column=2, padx=5)
        
        self.start_date.bind("<<DateEntrySelected>>", self.update_end_date_limit)
        
        # Sensor Type/ID
        ttk.Label(self.root, text="Sensor type/ID").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.sensor_type = ttk.Combobox(self.root, values=sensor_type_list, state='readonly')
        self.sensor_type.grid(row=1, column=1, padx=5)
        self.sensor_type.set('sds011')
        
        self.sensor_id = ttk.Entry(self.root)
        self.sensor_id.grid(row=1, column=2, padx=5)
        self.sensor_id.insert(0, '31128')
        
        # Configure grid weights to center the content
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_columnconfigure(2, weight=1)
        
        # New Labels for Sensor Title and Location
        self.sensor_title_label = ttk.Label(self.root, text="", font=("TkDefaultFont", 14, "bold"), anchor="center")
        self.sensor_title_label.grid(row=2, column=0, columnspan=3, pady=(10, 0), sticky="ew")
        self.location_info_label = ttk.Label(self.root, text="", font=("TkDefaultFont", 10), anchor="center")
        self.location_info_label.grid(row=3, column=0, columnspan=3, pady=(0, 10), sticky="ew")

        # Aktions-Buttons Frame
        action_buttons_frame = ttk.Frame(self.root)
        action_buttons_frame.grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")
        self.root.grid_columnconfigure(1, weight=1)

        self.download_btn = ttk.Button(action_buttons_frame, text="Download Data", command=self.load_data)
        self.download_btn.pack(side=tk.TOP, padx=5, pady=2, expand=True, fill=tk.X)
        
        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=5, column=0, columnspan=3, pady=(10, 5), sticky="ew", padx=5)
        
        # Status Label (moved to row 6)
        self.status_label = ttk.Label(self.root, text="")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)
        
    def update_sensor_and_location_labels(self):
        sensor_id = self.sensor_id.get()
        start_date = self.start_date.get_date()
        end_date = self.end_date.get_date()

        formatted_start_date = format_date_for_db(start_date)
        formatted_end_date = format_date_for_db(end_date)

        data = get_date_range_data(sensor_id, formatted_start_date, formatted_end_date)

        self.sensor_title_label.config(text=f"Sensor {sensor_id} Air Quality Data")

        if data:
            location = data[0].get('location', 'Unbekannt')
            lat = data[0].get('lat', None)
            lon = data[0].get('lon', None)
            
            location_text = ''
            if location and location != 'Unbekannt':
                location_text += f'Standort: {location}'
            if lat is not None and lon is not None:
                if location_text:
                    location_text += f' (Lat: {lat:.3f}, Lon: {lon:.3f})'
                else:
                    location_text += f'(Lat: {lat:.3f}, Lon: {lon:.3f})'
            self.location_info_label.config(text=location_text)
        else:
            self.location_info_label.config(text="") # Clear if no data

    def load_data(self):
        if not self.options_are_valid():
            messagebox.showerror("Error", CONST_NOT_ALL_FIELDS_FILLED)
            return
        
        # Disable download button and reset progress
        self.download_btn.config(state='disabled')
        self.progress_var.set(0)
        self.status_label.config(text="Bereite Download vor...")
        self.root.update()
        
        try:
            print(f"load data {self.sensor_type.get()} {self.sensor_id.get()}", 
                  self.start_date.get(), self.end_date.get())
            
            # Lade Daten herunter mit Progress Updates
            if self.download_data_with_progress(
                self.sensor_type.get(),
                self.sensor_id.get(),
                self.start_date.get(),
                self.end_date.get()
            ):
                self.status_label.config(text="Download erfolgreich abgeschlossen!")
                messagebox.showinfo("Erfolg", "Daten erfolgreich heruntergeladen und in Datenbank gespeichert!")
                self.update_sensor_and_location_labels() # Update labels after successful download
                self.refresh_diagram()
            else:
                self.status_label.config(text="Download fehlgeschlagen!")
                messagebox.showerror("Fehler", "Fehler beim Herunterladen oder Verarbeiten der Daten.")
        finally:
            # Re-enable download button
            self.download_btn.config(state='normal')
    
    def download_data_with_progress(self, sensor_type, sensor_id, start_date, end_date):
        """Download data with progress updates"""
        try:
            from src.download.downloader import download_csv_files
            from src.core.processing import process_csv_data
            from src.core.database import init_db, get_db_connection, print_database_stats
            import datetime
            
            self.status_label.config(text="Initialisiere Datenbank...")
            self.progress_var.set(10)
            self.root.update()
            
            init_db()
            
            self.status_label.config(text="Bereite Download vor...")
            self.progress_var.set(20)
            self.root.update()
            
            # Convert dates
            if isinstance(start_date, str):
                start_date = datetime.datetime.strptime(start_date, '%d.%m.%Y').date()
            if isinstance(end_date, str):
                end_date = datetime.datetime.strptime(end_date, '%d.%m.%Y').date()
            
            # Calculate total days for progress
            total_days = (end_date - start_date).days + 1
            
            self.status_label.config(text="Lade Daten herunter...")
            self.progress_var.set(30)
            self.root.update()
            
            downloaded_contents = download_csv_files(start_date, end_date, sensor_type, sensor_id, None)
            
            if not downloaded_contents:
                self.status_label.config(text="Keine neuen Daten zum Herunterladen gefunden.")
                self.progress_var.set(100)
                self.root.update()
                return True
            
            self.status_label.config(text="Verarbeite heruntergeladene Daten...")
            self.progress_var.set(50)
            self.root.update()
            
            conn = get_db_connection()
            c = conn.cursor()
            
            # Process each downloaded file with progress updates
            for i, (filename, csv_content) in enumerate(downloaded_contents):
                progress = 50 + (i / len(downloaded_contents)) * 40  # 50% to 90%
                self.progress_var.set(progress)
                self.status_label.config(text=f"Verarbeite {filename}... ({i+1}/{len(downloaded_contents)})")
                self.root.update()
                
                process_csv_data(conn, c, filename, csv_content)
            
            conn.close()
            
            self.status_label.config(text="Finalisiere...")
            self.progress_var.set(90)
            self.root.update()
            
            print_database_stats()
            
            self.progress_var.set(100)
            self.status_label.config(text="Download abgeschlossen!")
            self.root.update()
            
            return True
            
        except Exception as e:
            self.status_label.config(text=f"Fehler: {str(e)}")
            print(f"Error in download_data_with_progress: {e}")
            return False

    def refresh_diagram(self):
        if not self.options_are_valid():
            messagebox.showerror("Error", CONST_NOT_ALL_FIELDS_FILLED)
            return
            
        # Clear previous plot if exists
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and hasattr(widget, '_is_diagram_frame'):
                widget.destroy()

        # Update labels before plotting
        self.update_sensor_and_location_labels()
            
        # Get the figure from plotting module
        start_date = self.start_date.get_date().strftime('%Y-%m-%d')
        end_date = self.end_date.get_date().strftime('%Y-%m-%d')
        fig = plot_sensor_data(self.sensor_id.get(), start_date, end_date)
        if fig is None:
            messagebox.showerror("Error", "No data available for this sensor")
            return
            
        # Create a frame for the diagram to ensure proper packing and destruction
        diagram_frame = ttk.Frame(self.root)
        diagram_frame._is_diagram_frame = True # Mark this frame for easy identification
        diagram_frame.grid(row=7, column=0, columnspan=3, pady=(10, 0), sticky="nsew") # Reduced pady on top
        self.root.grid_rowconfigure(7, weight=1) # Make row 7 expandable

        # Add buttons frame at the top of the diagram frame
        button_frame = ttk.Frame(diagram_frame)
        button_frame.pack(side=tk.TOP, pady=0) # Reduced pady
        
        # Add save button
        save_btn = ttk.Button(button_frame, text="Speichern", command=lambda: self.save_diagram(fig))
        save_btn.pack(side=tk.LEFT, padx=5)
            
        # Create canvas and add it to the window
        canvas = FigureCanvasTkAgg(fig, master=diagram_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def save_diagram(self, fig):
        filetypes = [
            ('PDF Dateien', '*.pdf'),
            ('PNG Dateien', '*.png')
        ]
        filename = filedialog.asksaveasfilename(
            defaultextension='.pdf',
            filetypes=filetypes,
            title='Diagramm speichern'
        )
        if filename:
            fig.savefig(filename, bbox_inches='tight', dpi=300)
            messagebox.showinfo("Erfolg", "Diagramm wurde erfolgreich gespeichert!")

    def options_are_valid(self):
        if self.sensor_type.get() == "" or self.sensor_id.get() == "":
            return False
        return True

    def update_end_date_limit(self, event=None):
        new_start = self.start_date.get_date()
        yesterday = date.today() - timedelta(days=1)
        self.end_date.config(mindate=new_start, maxdate=yesterday)
        if self.end_date.get_date() < new_start:
            self.end_date.set_date(new_start)
        elif self.end_date.get_date() > yesterday:
            self.end_date.set_date(yesterday)

    def quit_app(self):
        """Beendet das Programm sauber"""
        plt.close('all')
        self.root.destroy()

    def reset_database(self):
        """Setzt die Datenbank zurück"""
        if messagebox.askyesno("Datenbank zurücksetzen", 
                             "Möchten Sie die Datenbank wirklich zurücksetzen?\nAlle gespeicherten Daten gehen verloren!"):
            from src.core.database import reset_database
            reset_database()
            messagebox.showinfo("Erfolg", "Datenbank wurde zurückgesetzt!")

def main():
    root = tk.Tk()
    app = SensorDataGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()