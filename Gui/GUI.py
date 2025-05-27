import tkinter as tk
from tkinter import filedialog, ttk
from tkcalendar import DateEntry
from datetime import date
from tkinter import messagebox
from center_window import center_window
from consts import CONST_NOT_ALL_FIELDS_FILLED
from consts import sensor_type_list


def pick_save_folder():
    folder_selected = filedialog.askdirectory()
    target_folder_var.set(folder_selected)

def load_data():
    if not options_are_valid():
        messagebox.showerror("Error", CONST_NOT_ALL_FIELDS_FILLED)
        return
    print(f"load data {target_folder_var.get()} {sensor_type.get()} {sensor_id.get()}", start_date.get(), end_date.get(), target_folder_var.get())

def load_data_2():
    if not options_are_valid():
        messagebox.showerror("Error",CONST_NOT_ALL_FIELDS_FILLED)
        return
    print("Button 2")

def refresh_diagram():
    if not options_are_valid():
        messagebox.showerror("Error",CONST_NOT_ALL_FIELDS_FILLED)
        return
    print("refresh diagram")

def options_are_valid():
    if sensor_type.get() == "" or sensor_id.get()  == "" or target_folder_var.get()  == "":
        return False
    return True



root = tk.Tk()
root.title("GUI concept")

target_folder_var = tk.StringVar()

tk.Label(root, text="Date range").grid(row=0, column=0, sticky="w", padx=5, pady=5)

start_date = DateEntry(
    root,
    date_pattern='dd.MM.yyyy',
    state='readonly',
    maxdate=date.today()
)
start_date.grid(row=0, column=1, padx=5)

end_date = DateEntry(
    root,
    date_pattern='dd.MM.yyyy',
    state='readonly',
    mindate=start_date.get_date(),
    maxdate=date.today()
)
end_date.grid(row=0, column=2, padx=5)

def update_end_date_limit(event):
    new_start = start_date.get_date()
    end_date.config(mindate=new_start)
    if end_date.get_date() < new_start:
        end_date.set_date(new_start)

start_date.bind("<<DateEntrySelected>>", update_end_date_limit)

tk.Label(root, text="Sensor type/ID").grid(row=1, column=0, sticky="w", padx=5, pady=5)
sensor_type = ttk.Combobox(root, values=sensor_type_list, state='readonly')
sensor_type.grid(row=1, column=1, padx=5)
sensor_id = ttk.Entry(root)
sensor_id.grid(row=1, column=2, padx=5)

tk.Label(root, text="target folder").grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_target_folder = tk.Entry(root, textvariable=target_folder_var, width=40, state='readonly')
entry_target_folder.grid(row=2, column=1, padx=5)
btn_pick_folder = tk.Button(root, text="...", command=pick_save_folder)
btn_pick_folder.grid(row=2, column=2, padx=5)

tk.Label(root, text="load data").grid(row=3, column=0, sticky="w", padx=5, pady=5)
btn_load = tk.Button(root, text="Load 1", command=load_data)
btn_load.grid(row=3, column=1, padx=5)
btn_load_2 = tk.Button(root, text="Load 2", command=load_data_2)
btn_load_2.grid(row=3, column=2, padx=5)

btn_refresh_diagram = tk.Button(root, text="refresh diagram", command=refresh_diagram)
btn_refresh_diagram.grid(row=4, column=2, sticky="e", padx=5, pady=10)
root.update()       
center_window(root)
root.mainloop()