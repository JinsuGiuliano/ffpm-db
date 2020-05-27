import sqlite3
import csv
import pandas as pd



with open('bf.csv', 'r') as file:
    reader = csv.reader(file)
    nf = []
    for row in reader:
        line = str(row[0]).replace(";",",")
        nf.append(line)

with open('bef.csv', 'w') as new_file:
    writer = csv.writer(new_file)
    writer.writerow(nf)


               

           