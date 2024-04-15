import tkinter as tk
from tkinter import ttk, messagebox
from math import sqrt

window = tk.Tk()
window.title("Right Triangle Calculator")
window.geometry("300x150")

frame = ttk.Frame(window, padding="10 10 10 10")
frame.pack(fill="both", expand=True)


def clicked_calc_button():
    try:
        a = float(sideA_text.get())
        b = float(sideB_text.get())

        c = sqrt(a ** 2 + b ** 2)
        sideC_text.set(str(f"{c:.3f}"))
    except ValueError:
        messagebox.showwarning("An Error Occurred", "Please Enter Integer or Float Values")


def clicked_exit_button():
    window.destroy()


# Labels
sideA_label = ttk.Label(frame, text="Side A:")
sideA_label.grid(column=0, row=0)
sideB_label = ttk.Label(frame, text="Side B:")
sideB_label.grid(column=0, row=1)
sideC_label = ttk.Label(frame, text="Side C:")
sideC_label.grid(column=0, row=2)

# Entry Boxes
sideA_text = tk.StringVar()
sideA_input = ttk.Entry(frame, width=25, textvariable=sideA_text)
sideA_input.grid(column=1, row=0, columnspan=2)

sideB_text = tk.StringVar()
sideB_input = ttk.Entry(frame, width=25, textvariable=sideB_text)
sideB_input.grid(column=1, row=1, columnspan=2)

sideC_text = tk.StringVar()
sideC_input = ttk.Entry(frame, width=25, textvariable=sideC_text, state="readonly")
sideC_input.grid(column=1, row=2, columnspan=2)

# Buttons
calc_button = ttk.Button(frame, text="Calculate", command=clicked_calc_button)
calc_button.grid(column=1, row=3)

exit_button = ttk.Button(frame, text="Exit", command=clicked_exit_button)
exit_button.grid(column=2, row=3)

for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=3)

window.mainloop()
