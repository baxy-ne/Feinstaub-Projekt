import tkinter as tk
from tkinter import filedialog, ttk
from tkcalendar import DateEntry
from datetime import date


def ordner_waehlen():
    folder_selected = filedialog.askdirectory()
    zielordner_var.set(folder_selected)

def daten_laden_1():
    print(f"Daten Laden 1 {zielordner_var.get()}, {sensor_typ.get()}, {sensor_id.get()}", start_datum.get(), end_datum.get())

def daten_laden_2():
    print("Daten Laden 2")

def diagramm_akt():
    print("Diagramm aktualisieren")

root = tk.Tk()
root.title("GUI Konzept")

zielordner_var = tk.StringVar()

tk.Label(root, text="DatumBereich").grid(row=0, column=0, sticky="w", padx=5, pady=5)

start_datum = DateEntry(
    root,
    date_pattern='dd.MM.yyyy',
    state='readonly',
    maxdate=date.today()
)
start_datum.grid(row=0, column=1, padx=5)

end_datum = DateEntry(
    root,
    date_pattern='dd.MM.yyyy',
    state='readonly',
    mindate=start_datum.get_date(),
    maxdate=date.today()
)
end_datum.grid(row=0, column=2, padx=5)

def update_end_date_limit(event):
    new_start = start_datum.get_date()
    end_datum.config(mindate=new_start)
    if end_datum.get_date() < new_start:
        end_datum.set_date(new_start)

start_datum.bind("<<DateEntrySelected>>", update_end_date_limit)

tk.Label(root, text="SensorTyp/ID").grid(row=1, column=0, sticky="w", padx=5, pady=5)
sensor_typ = ttk.Combobox(root, values=["bme280", 
                                        "bmp180", "bmp280","ds18b20", "dht22", "hpm", "htu21d", "laerm", 
                                        "pms1003", "pms3003", "pms5003", "pms7003", "ppd42ns", 
                                        "radiation_sbm-19","radiation_sbm-20","radiation_si22g",
                                        "sds011","sdc30","sht15","sht30","sht31","sht35","sht85","sps30", ], state='readonly')
sensor_typ.grid(row=1, column=1, padx=5)
sensor_id = ttk.Entry(root)
sensor_id.grid(row=1, column=2, padx=5)

tk.Label(root, text="ZielOrdner").grid(row=2, column=0, sticky="w", padx=5, pady=5)
zielordner_entry = tk.Entry(root, textvariable=zielordner_var, width=40, state='readonly')
zielordner_entry.grid(row=2, column=1, padx=5)
ordner_button = tk.Button(root, text="...", command=ordner_waehlen)
ordner_button.grid(row=2, column=2, padx=5)

tk.Label(root, text="DatenLaden").grid(row=3, column=0, sticky="w", padx=5, pady=5)
laden_button1 = tk.Button(root, text="Laden 1", command=daten_laden_1)
laden_button1.grid(row=3, column=1, padx=5)
laden_button2 = tk.Button(root, text="Laden 2", command=daten_laden_2)
laden_button2.grid(row=3, column=2, padx=5)

diagramm_button = tk.Button(root, text="Diagramm Akt.", command=diagramm_akt)
diagramm_button.grid(row=4, column=2, sticky="e", padx=5, pady=10)

root.mainloop()