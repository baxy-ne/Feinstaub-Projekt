import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
from src.core.view_model import download_data, process_data
from src.core.consts import CONST_NOT_ALL_FIELDS_FILLED, sensor_type_list
from src.gui.utils import center_window
from src.core.plotting import plot_sensor_data
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SensorDataGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI concept")
        self.root.geometry("600x200")
        center_window(self.root)
        
        # Bindet das Schließen des Fensters an die quit_app Methode
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        
        self.target_folder_var = tk.StringVar()
        
        # Date Range
        ttk.Label(self.root, text="Date range").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.start_date = DateEntry(
            self.root,
            date_pattern='dd.MM.yyyy',
            state='readonly',
            maxdate=date.today()
        )
        self.start_date.grid(row=0, column=1, padx=5)
        
        self.end_date = DateEntry(
            self.root,
            date_pattern='dd.MM.yyyy',
            state='readonly',
            mindate=self.start_date.get_date(),
            maxdate=date.today()
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
        
        # Target Folder
        ttk.Label(self.root, text="target folder").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.folder_entry = ttk.Entry(self.root, textvariable=self.target_folder_var, width=40, state='readonly')
        self.folder_entry.grid(row=2, column=1, padx=5)
        self.folder_btn = ttk.Button(self.root, text="...", command=self.pick_save_folder)
        self.folder_btn.grid(row=2, column=2, padx=5)
        
        # Buttons
        ttk.Label(self.root, text="load data").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.download_btn = ttk.Button(self.root, text="Download Data", command=self.load_data)
        self.download_btn.grid(row=3, column=1, padx=5)
        self.process_btn = ttk.Button(self.root, text="Save Data to DB", command=self.load_data_2)
        self.process_btn.grid(row=3, column=2, padx=5)
        
        # Reset Button
        self.reset_btn = ttk.Button(self.root, text="Reset DB", command=self.reset_database)
        self.reset_btn.grid(row=3, column=3, padx=5)
        
        # Diagram Button
        self.diagram_btn = ttk.Button(self.root, text="show diagram", command=self.refresh_diagram)
        self.diagram_btn.grid(row=4, column=2, sticky="e", padx=5, pady=10)
        
        # Status Label
        self.status_label = ttk.Label(self.root, text="")
        self.status_label.grid(row=5, column=0, columnspan=3, pady=10)
        
    def pick_save_folder(self):
        folder_selected = filedialog.askdirectory()
        self.target_folder_var.set(folder_selected)

    def load_data(self):
        if not self.options_are_valid():
            messagebox.showerror("Error", CONST_NOT_ALL_FIELDS_FILLED)
            return
        print(f"load data {self.target_folder_var.get()} {self.sensor_type.get()} {self.sensor_id.get()}", 
              self.start_date.get(), self.end_date.get(), self.target_folder_var.get())
        download_data(
            self.sensor_type.get(),
            self.sensor_id.get(),
            self.start_date.get(),
            self.end_date.get(),
            self.target_folder_var.get()
        )

    def load_data_2(self):
        if not self.options_are_valid():
            messagebox.showerror("Error", CONST_NOT_ALL_FIELDS_FILLED)
            return
        print("Button 2")
        process_data(self.target_folder_var.get())

    def refresh_diagram(self):
        if not self.options_are_valid():
            messagebox.showerror("Error", CONST_NOT_ALL_FIELDS_FILLED)
            return
            
        # Create a new window for the diagram
        diagram_window = tk.Toplevel(self.root)
        diagram_window.title(f"Sensor {self.sensor_id.get()} Data")
        diagram_window.geometry("1200x1000")  # Fensterhöhe erhöht
        center_window(diagram_window)
        
        # Get the figure from plotting module
        start_date = self.start_date.get_date().strftime('%Y-%m-%d')
        end_date = self.end_date.get_date().strftime('%Y-%m-%d')
        fig = plot_sensor_data(self.sensor_id.get(), start_date, end_date)
        if fig is None:
            messagebox.showerror("Error", "No data available for this sensor")
            diagram_window.destroy()
            return
            
        # Add buttons frame at the top
        button_frame = ttk.Frame(diagram_window)
        button_frame.pack(side=tk.TOP, pady=10)
        
        # Add save button
        save_btn = ttk.Button(button_frame, text="Speichern", command=lambda: self.save_diagram(fig))
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # Add close button
        close_btn = ttk.Button(button_frame, text="Schließen", command=diagram_window.destroy)
        close_btn.pack(side=tk.LEFT, padx=5)
            
        # Create canvas and add it to the window
        canvas = FigureCanvasTkAgg(fig, master=diagram_window)
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
        if self.sensor_type.get() == "" or self.sensor_id.get() == "" or self.target_folder_var.get() == "":
            return False
        return True

    def update_end_date_limit(self, event=None):
        new_start = self.start_date.get_date()
        today = date.today()
        self.end_date.config(mindate=new_start, maxdate=today)
        if self.end_date.get_date() < new_start:
            self.end_date.set_date(new_start)
        elif self.end_date.get_date() > today:
            self.end_date.set_date(today)

    def quit_app(self):
        """Beendet das Programm sauber"""
        plt.close('all')  # Schließt alle Matplotlib-Fenster
        self.root.destroy()  # Schließt das Hauptfenster

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