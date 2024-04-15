import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, date

sales_window = tk.Tk()
sales_window.title("Edit Sales Amount")
sales_window.geometry("400x300")

frame = ttk.Frame(sales_window, padding="10")
frame.pack(fill="both", expand=True)

desc = ttk.Label(frame, text="Enter date and Region to get sales amount.")
desc.grid(row=0, column=0, columnspan=4)

dateVar = tk.StringVar()
date_label = ttk.Label(frame, text="Date:")
date_label.grid(row=1, column=0, sticky=tk.E)
date_entry = ttk.Entry(frame, textvariable=dateVar, width=25)
date_entry.grid(row=1, column=1)

region = tk.StringVar()
region_label = ttk.Label(frame, text="Region:")
region_label.grid(row=2, column=0, sticky=tk.E)
region_entry = ttk.Entry(frame, textvariable=region, width=25)
region_entry.grid(row=2, column=1)

amount = tk.StringVar()
amount_label = ttk.Label(frame, text="Amount:")
amount_label.grid(row=3, column=0, sticky=tk.E)
amount_entry = ttk.Entry(frame, textvariable=amount, width=25)
amount_entry.grid(row=3, column=1)

saleID = tk.IntVar()
saleID_label = ttk.Label(frame, text="ID:")
saleID_label.grid(row=4, column=0, sticky=tk.E)
saleID_entry = ttk.Entry(frame, textvariable=saleID, width=25, state="readonly")
saleID_entry.grid(row=4, column=1)


def connect_to_db():
    conn = sqlite3.connect("sales_db.sqlite")
    conn.row_factory = sqlite3.Row
    return conn


def close(conn):
    if conn:
        conn.close()


def validate_date():

    """Validates the date and returns True if its good and False if not"""
    check_date = date_entry.get()

    check_format = check_date.split('-')
    for i, num in enumerate(check_format):
        if not num.isnumeric():
            return False
        elif i == 0 and len(num) > 4:
            return False
        elif i == 1 and len(num) > 2:
            return False
        elif i == 2 and len(num) > 2:
            return False

    if datetime.strptime(check_date, "%Y-%m-%d") > datetime.now():
        return False

    return True


def get_regions(conn):
    """ Gathers the list of regions from the database and returns them """
    convert = []
    query = """SELECT * FROM Region"""
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()

    for row in results:
        convert.append(row)

    valid = []
    for row in convert:
        valid.append(row["code"])
    return valid


def validate_region(conn):
    """Validates the region and returns True if its good and False if not"""

    valid = get_regions(conn)

    if region_entry.get() not in valid:
        return False
    else:
        return True


def get_amount():

    """ function for the get amount button, validates the information, and returns the amount as well as the ID"""
    conn = connect_to_db()
    regions = get_regions(conn)
    regions = ", ".join(regions)
    total = 0

    if not validate_date():
        messagebox.showerror("Error", "Invalid date. Must be YYYY-MM-DD and a valid date")
        dateVar.set('')

    elif not validate_region(conn):
        messagebox.showerror("Error", f"Invalid Region must be in {regions}")
        region.set('')

    elif date_entry == '' or region_entry == '':
        messagebox.showerror("Error", "Date and/or Region must be filled in.")

    else:
        query = """SELECT * FROM Sales WHERE salesDate = ? AND region = ?"""
        cur = conn.cursor()
        cur.execute(query, (date_entry.get(), region_entry.get()))
        results = cur.fetchall()

        sales = []
        for row in results:
            sales.append(row)

        for sale in sales:
            total += int(sale[1])
            saleID.set(sale[0])

        if total == 0:
            messagebox.showerror("Error", "No sales found for given region and date")

        amount.set(f"{total:.2f}")


def save_changes():
    """ Allows user to save changes they have made to the amount to the database"""
    conn = connect_to_db()
    regions = get_regions(conn)
    regions = ", ".join(regions)

    if float(amount_entry.get()) < 0:
        messagebox.showerror("Error", "Sales amount must be greater than 0")

    else:
        query = """UPDATE Sales SET ammount = ? WHERE ID = ?"""
        cur = conn.cursor()
        cur.execute(query, (amount_entry.get(), saleID_entry.get()))
        conn.commit()
        messagebox.showinfo("Updated!", "Sales amount has been updated.")


amount_button = ttk.Button(frame, text="Get Amount", command=get_amount)
amount_button.grid(row=2, column=2)

for child in frame.winfo_children():
    child.grid(padx=3, pady=3)

change_button = ttk.Button(frame, text="Save Changes", command=save_changes)
change_button.grid(row=5, column=1, sticky=tk.W)

exit_button = ttk.Button(frame, text="Exit", command=frame.quit)
exit_button.grid(row=5, column=1, sticky=tk.E)

sales_window.mainloop()
