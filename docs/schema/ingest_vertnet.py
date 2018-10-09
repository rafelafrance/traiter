import sqlite3
import csv
import json
import pandas as pd

CSV_FILE = '../data/vn_20151028_orems_fnotes_dprops_not_null_grouped.csv'
DB_FILE  = '../data/traits.db'


with open(CSV_FILE, 'r') as csv_file, sqlite3.connect(DB_FILE) as conn:
    cursor = conn.cursor()
    reader = csv.DictReader(csv_file)
    for row in reader:
        print(reader.line_num)
