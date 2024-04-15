import csv
import sqlite3

print("Customer Data Importer\n")

csv_file = input("CSV file:\t")
db_file = input("DB file:\t")
table_name = input("Table name:\t")

# Deletes all data from the database
conn = sqlite3.connect(db_file)
c = conn.cursor()
query = """DELETE FROM {}""".format(table_name)
c.execute(query)
conn.commit()

# Program waits for user input before continuing to repopulation
print(f"\nAll old rows deleted from {table_name} table.")

# Repopulates the database from csv file. Count variable to track number of rows
count = 0
with open(csv_file, "r") as file:
    reader = csv.reader(file)
    next(reader)
    for i, row in enumerate(reader):
        query = f"""INSERT INTO {table_name} VALUES ('{101 + i}', '{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}')"""
        c.execute(query)
        conn.commit()
        count += 1

print(f"{count} row(s) inserted into {table_name} table.")

conn.close()
