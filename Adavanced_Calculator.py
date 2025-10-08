import tkinter as tk
import math

# --- Functions ---
memory = 0

def click(value):
    entry.insert(tk.END, value)

def clear():
    entry.delete(0, tk.END)

def all_clear():
    entry.delete(0, tk.END)
    global memory
    memory = 0

def calculate():
    try:
        expr = entry.get().replace("^", "**")
        result = eval(expr, {"__builtins__": None}, math.__dict__)
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

def memory_clear():
    global memory
    memory = 0

def memory_recall():
    entry.insert(tk.END, str(memory))

def memory_add():
    global memory
    try:
        memory += float(entry.get())
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

def memory_subtract():
    global memory
    try:
        memory -= float(entry.get())
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

# --- Hover effects ---
def on_enter(button, color):
    button['bg'] = color

def on_leave(button, color):
    button['bg'] = color

# --- Main Window ---
root = tk.Tk()
root.title("Scientific Calculator")
root.configure(bg="#2c3e50")
root.resizable(False, False)

# --- Entry Field ---
entry = tk.Entry(root, font=('Helvetica', 24), bd=0, bg="#ecf0f1", fg="#2c3e50", justify='right')
entry.grid(row=0, column=0, columnspan=6, padx=10, pady=20, ipady=10)

# --- Button Colors ---
button_bg = "#34495e"
button_hover = "#3d566e"
button_fg = "#ecf0f1"

operator_bg = "#e67e22"
operator_hover = "#eb8c3a"
operator_fg = "#ffffff"

clear_bg = "#c0392b"
clear_hover = "#e74c3c"
clear_fg = "#ffffff"

# --- Buttons ---
buttons = [
    ('7',1,0),('8',1,1),('9',1,2),('/',1,3),('sin(',1,4),('cos(',1,5),
    ('4',2,0),('5',2,1),('6',2,2),('*',2,3),('tan(',2,4),('log(',2,5),
    ('1',3,0),('2',3,1),('3',3,2),('-',3,3),('sqrt(',3,4),('^',3,5),
    ('0',4,0),('.',4,1),('(',4,2),(')',4,3),('+',4,4),('exp(',4,5),
    ('C',5,0),('AC',5,1),('=',5,2),('M+',5,3),('M-',5,4),('MR',5,5)
]

for (text, row, col) in buttons:
    if text == "=":
        b = tk.Button(root, text=text, bg=operator_bg, fg=operator_fg, font=('Helvetica', 18), bd=0, command=calculate)
        b.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
        b.bind("<Enter>", lambda e,b=b: on_enter(b, operator_hover))
        b.bind("<Leave>", lambda e,b=b: on_leave(b, operator_bg))
    elif text == "C":
        b = tk.Button(root, text=text, bg=clear_bg, fg=clear_fg, font=('Helvetica', 18), bd=0, command=clear)
        b.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
        b.bind("<Enter>", lambda e,b=b: on_enter(b, clear_hover))
        b.bind("<Leave>", lambda e,b=b: on_leave(b, clear_bg))
    elif text == "AC":
        b = tk.Button(root, text=text, bg=clear_bg, fg=clear_fg, font=('Helvetica', 18), bd=0, command=all_clear)
        b.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
        b.bind("<Enter>", lambda e,b=b: on_enter(b, clear_hover))
        b.bind("<Leave>", lambda e,b=b: on_leave(b, clear_bg))
    elif text == "M+":
        b = tk.Button(root, text=text, bg=operator_bg, fg=operator_fg, font=('Helvetica', 18), bd=0, command=memory_add)
        b.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
        b.bind("<Enter>", lambda e,b=b: on_enter(b, operator_hover))
        b.bind("<Leave>", lambda e,b=b: on_leave(b, operator_bg))
    elif text == "M-":
        b = tk.Button(root, text=text, bg=operator_bg, fg=operator_fg, font=('Helvetica', 18), bd=0, command=memory_subtract)
        b.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
        b.bind("<Enter>", lambda e,b=b: on_enter(b, operator_hover))
        b.bind("<Leave>", lambda e,b=b: on_leave(b, operator_bg))
    elif text == "MR":
        b = tk.Button(root, text=text, bg=operator_bg, fg=operator_fg, font=('Helvetica', 18), bd=0, command=memory_recall)
        b.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
        b.bind("<Enter>", lambda e,b=b: on_enter(b, operator_hover))
        b.bind("<Leave>", lambda e,b=b: on_leave(b, operator_bg))
    else:
        b = tk.Button(root, text=text, bg=button_bg, fg=button_fg, font=('Helvetica', 18), bd=0, command=lambda t=text: click(t))
        b.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
        b.bind("<Enter>", lambda e,b=b: on_enter(b, button_hover))
        b.bind("<Leave>", lambda e,b=b: on_leave(b, button_bg))

# --- Make buttons expand ---
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
for i in range(6):
    root.grid_columnconfigure(i, weight=1)

root.mainloop()
