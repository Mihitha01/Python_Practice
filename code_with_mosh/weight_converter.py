import tkinter as tk
from tkinter import ttk

def convert_weight():
    try:
        weight = float(weight_entry.get())
        unit = unit_var.get()

        if unit == "Lbs":
            converted = weight * 0.45
            result_label.config(text=f"{converted:.2f} Kilograms")
        else:
            converted = weight / 0.45
            result_label.config(text=f"{converted:.2f} Pounds")
    except ValueError:
        result_label.config(text="Please enter a valid number.")

# Create main window
root = tk.Tk()
root.title("Weight Converter")
root.geometry("300x200")
root.resizable(False, False)

# Label and Entry
ttk.Label(root, text="Enter Weight:").pack(pady=5)
weight_entry = ttk.Entry(root)
weight_entry.pack(pady=5)

# Dropdown for unit selection
unit_var = tk.StringVar(value="Lbs")
unit_dropdown = ttk.Combobox(root, textvariable=unit_var, values=["Lbs", "Kg"], state="readonly")
unit_dropdown.pack(pady=5)

# Convert button
convert_button = ttk.Button(root, text="Convert", command=convert_weight)
convert_button.pack(pady=10)

# Result label
result_label = ttk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()
