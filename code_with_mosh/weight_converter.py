import customtkinter as ctk

# Set appearance
ctk.set_appearance_mode("system")  # "light" or "dark"
ctk.set_default_color_theme("blue")

# Conversion rates to kilograms
CONVERSION_RATES = {
    "Kilograms (kg)": 1,
    "Pounds (lb)": 0.453592,
    "Grams (g)": 0.001,
    "Ounces (oz)": 0.0283495,
    "Stones (st)": 6.35029
}

def convert_weight(*args):
    try:
        value = float(weight_entry.get())
        from_unit = from_unit_var.get()
        to_unit = to_unit_var.get()

        # Convert to kg first, then to target unit
        weight_in_kg = value * CONVERSION_RATES[from_unit]
        converted = weight_in_kg / CONVERSION_RATES[to_unit]

        result_label.configure(
            text=f"{value:.2f} {from_unit.split()[0]} = {converted:.2f} {to_unit.split()[0]}"
        )
    except ValueError:
        result_label.configure(text="Enter a valid number")

def clear_fields():
    weight_entry.delete(0, "end")
    result_label.configure(text="")

# Create main window
app = ctk.CTk()
app.title("⚖️ Advanced Weight Converter")
app.geometry("420x350")
app.resizable(False, False)

# Title
title_label = ctk.CTkLabel(
    app, text="Weight Converter", font=ctk.CTkFont(size=22, weight="bold")
)
title_label.pack(pady=15)

# Frame for input fields
frame = ctk.CTkFrame(app)
frame.pack(padx=20, pady=10, fill="both", expand=True)

# Weight input
weight_label = ctk.CTkLabel(frame, text="Enter Weight:")
weight_label.pack(pady=(10, 5))
weight_entry = ctk.CTkEntry(frame, placeholder_text="e.g. 75")
weight_entry.pack(pady=5)

# Unit selection
from_unit_var = ctk.StringVar(value="Kilograms (kg)")
to_unit_var = ctk.StringVar(value="Pounds (lb)")

unit_frame = ctk.CTkFrame(frame)
unit_frame.pack(pady=10)

from_unit_menu = ctk.CTkOptionMenu(unit_frame, variable=from_unit_var, values=list(CONVERSION_RATES.keys()))
from_unit_menu.pack(side="left", padx=5)

arrow_label = ctk.CTkLabel(unit_frame, text="→", font=ctk.CTkFont(size=18))
arrow_label.pack(side="left", padx=5)

to_unit_menu = ctk.CTkOptionMenu(unit_frame, variable=to_unit_var, values=list(CONVERSION_RATES.keys()))
to_unit_menu.pack(side="left", padx=5)

# Convert and Clear buttons
button_frame = ctk.CTkFrame(frame)
button_frame.pack(pady=10)

convert_button = ctk.CTkButton(button_frame, text="Convert", command=convert_weight)
convert_button.pack(side="left", padx=10)

clear_button = ctk.CTkButton(button_frame, text="Clear", fg_color="gray", command=clear_fields)
clear_button.pack(side="left", padx=10)

# Result label
result_label = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=16, weight="bold"))
result_label.pack(pady=10)

# Auto update when Enter key pressed
app.bind("<Return>", convert_weight)

# Run the app
app.mainloop()
