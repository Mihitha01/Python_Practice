import tkinter as tk

# Functions
def click(button_text):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + button_text)

def clear():
    entry.delete(0, tk.END)

def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

# Hover effect functions
def on_enter(button, color):
    button['bg'] = color

def on_leave(button, color):
    button['bg'] = color

# Create main window
root = tk.Tk()
root.title("Calculator")
root.configure(bg="#2c3e50")
root.resizable(False, False)

# Entry field
entry = tk.Entry(root, width=16, font=('Helvetica', 28), bd=0, bg="#ecf0f1", fg="#2c3e50", justify='right')
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=20, ipady=10)

# Button colors
button_bg = "#34495e"
button_hover = "#3d566e"
button_fg = "#ecf0f1"

operator_bg = "#e67e22"
operator_hover = "#eb8c3a"
operator_fg = "#ffffff"

clear_bg = "#c0392b"
clear_hover = "#e74c3c"
clear_fg = "#ffffff"

# Button layout
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
    ('C', 5, 0)
]

# Create buttons
for (text, row, col) in buttons:
    if text == "=":
        b = tk.Button(root, text=text, bg=operator_bg, fg=operator_fg, font=('Helvetica', 22),
                      bd=0, command=calculate)
        b.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        b.bind("<Enter>", lambda e, b=b: on_enter(b, operator_hover))
        b.bind("<Leave>", lambda e, b=b: on_leave(b, operator_bg))
    elif text == "C":
        b = tk.Button(root, text=text, bg=clear_bg, fg=clear_fg, font=('Helvetica', 22),
                      bd=0, command=clear)
        b.grid(row=row, column=col, columnspan=4, sticky="nsew", padx=5, pady=5)
        b.bind("<Enter>", lambda e, b=b: on_enter(b, clear_hover))
        b.bind("<Leave>", lambda e, b=b: on_leave(b, clear_bg))
    elif text in ('/', '*', '-', '+'):
        b = tk.Button(root, text=text, bg=operator_bg, fg=operator_fg, font=('Helvetica', 22),
                      bd=0, command=lambda t=text: click(t))
        b.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        b.bind("<Enter>", lambda e, b=b: on_enter(b, operator_hover))
        b.bind("<Leave>", lambda e, b=b: on_leave(b, operator_bg))
    else:
        b = tk.Button(root, text=text, bg=button_bg, fg=button_fg, font=('Helvetica', 22),
                      bd=0, command=lambda t=text: click(t))
        b.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        b.bind("<Enter>", lambda e, b=b: on_enter(b, button_hover))
        b.bind("<Leave>", lambda e, b=b: on_leave(b, button_bg))

# Make buttons expand to fill grid cell
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

root.mainloop()
