from dataclasses import dataclass
from datetime import datetime, date
import csv
import sqlite3


DATE_FORMAT = '%Y-%m-%d'


def connect_to_db():
    conn = sqlite3.connect("sales_db.sqlite")
    conn.row_factory = sqlite3.Row
    return conn


def close(conn):
    if conn:
        conn.close()


def read_csv(file_name):
    csv_list = []
    with open(file_name, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            csv_list.append(row)
    return csv_list


@dataclass
class Region:
    code: str = ""
    name: str = ""


@dataclass
class Regions:
    valid: list

    def add(self, conn):
        self.valid = []
        query = """SELECT * FROM Region"""
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall()

        for row in results:
            self.valid.append(row)
        return self.valid

    def get_region(self, code):
        for row in self.valid:
            if row['code'] == code:
                return Region(row["code"], row["name"])

    def display(self):
        print("Valid codes: ", end="")
        for region in self.valid:
            print(region['code'], end=" ")


@dataclass
class File:
    filename: str = ""
    region: Region = None

    def get_region_code(self):
        sales = read_csv(self.filename)
        self.region = Region(sales[0][2])
        return self.region.code

    def validate(self):
        if self.filename.endswith('.csv'):
            return self.filename
        else:
            print("Invalid file format. Must be 'filename.csv'")


@dataclass
class DailySales:
    saleID: int = 0
    amount: float = 0.0
    date: date = datetime.now()
    region: Region = None
    quarter: int = 0.0

    def from_db(self, conn):
        query = "SELECT * FROM Sales"
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall()

        sales = []
        for row in results:
            sales.append(row)
        return sales

    def to_db(self, conn):
        query = "INSERT INTO SALES VALUES (NULL, ?, ?, ?)"
        cur = conn.cursor()
        cur.execute(query, (self.amount, datetime.strftime(self.date, DATE_FORMAT), self.region.code))
        conn.commit()

    def from_csv(self, sale):
        self.amount = float(sale[0].replace(',', ''))
        self.date = datetime.strptime(sale[1], DATE_FORMAT)
        self.region = Region(sale[2])
        self.get_quarter()

    def to_csv(self):
        sale = [self.amount, datetime.strftime(self.date, DATE_FORMAT), self.region.code]
        return sale

    def get_quarter(self):
        if self.date.month in [1, 2, 3]:
            self.quarter = 1
        elif self.date.month in [4, 5, 6]:
            self.quarter = 2
        elif self.date.month in [7, 8, 9]:
            self.quarter = 3
        else:
            self.quarter = 4

    def validate(self, valid):
        if self.amount < 0:
            return False
        elif self.date > datetime.now():
            return False
        elif self.region.code not in valid:
            return False
        else:
            return True


@dataclass
class SalesList:
    sales_list: list
    data: bool = True

    def add_sale(self, imported_list, valid):
        for sale in imported_list:
            new_sale = DailySales()
            new_sale.from_db(sale)
            if new_sale.validate(valid):
                self.sales_list.append(new_sale)
            else:
                print("One or more sales have invalid inputs.")

    def get_sale(self, user_input):
        for i, sale in enumerate(self.sales_list):
            if i == user_input:
                return sale

    def combine_sales(self, other_sales):
        self.sales_list.append(other_sales.sales_list)

    def get_count(self):
        return len(self.sales_list)
