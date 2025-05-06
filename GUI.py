import tkinter as tk
from tkinter import filedialog, ttk
from tkcalendar import DateEntry

def ordner_waehlen():
    folder_selected = filedialog.askdirectory()
    zielordner_var.set(folder_selected)

def daten_laden_1():
    print("Daten Laden 1")

def daten_laden_2():
    print("Daten Laden 2")

def diagramm_akt():
    print("Diagramm aktualisieren")

root = tk.Tk()
root.title("GUI Konzept")

zielordner_var = tk.StringVar()

tk.Label(root, text="DatumBereich").grid(row=0, column=0, sticky="w", padx=5, pady=5)
start_datum = DateEntry(root)
start_datum.grid(row=0, column=1, padx=5)
end_datum = DateEntry(root)
end_datum.grid(row=0, column=2, padx=5)

tk.Label(root, text="SensorTyp/ID").grid(row=1, column=0, sticky="w", padx=5, pady=5)
sensor_typ = ttk.Combobox(root, values=["Typ A", "Typ B"])
sensor_typ.grid(row=1, column=1, padx=5)
sensor_id = ttk.Combobox(root, values=["ID 001", "ID 002"])
sensor_id.grid(row=1, column=2, padx=5)

tk.Label(root, text="ZielOrdner").grid(row=2, column=0, sticky="w", padx=5, pady=5)
zielordner_entry = tk.Entry(root, textvariable=zielordner_var, width=40)
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