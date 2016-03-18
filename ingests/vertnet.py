import sqlite3
import csv
from pprint import pprint

CSV_FILE = '../data/vn_20151028_orems_fnotes_dprops_not_null_grouped.csv'
DB_FILE = '../data/vn_20151028_orems_fnotes_dprops_not_null_grouped.db'

print(sqlite3.sqlite_version)


with open(CSV_FILE, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        pprint(row)
        break
