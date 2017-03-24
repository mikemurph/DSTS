#imports
# from flask import Flask, render_template, request, json, g
import sqlite3 as sql
import csv

conn = sql.connect("sdn.db")
cursor = conn.cursor()

try:
    cursor.execute("""CREATE TABLE sdn
                      (a text, b text, c text, 
                       d text, e text, f text, g text, h text, i text, j text, k text, l text) 
                   """)
except:
    pass



# THIS ONE TAUGHT YOU EVERYTHING:::::; 
# https://www.blog.pythonlibrary.org/2012/07/18/python-a-simple-step-by-step-sqlite-tutorial/


# http://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python



with open('sdn_mod.csv', 'r') as file:
  reader = csv.DictReader(file)
  to_db = [(i['a'], i['b'], i['c'], i['d'], i['e'], i['f'], i['g'], i['h'], i['i'], i['j'], i['k'], i['l']) for i in reader]

cursor.executemany("INSERT INTO sdn VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", to_db)
conn.commit()

query_string = "SELECT * FROM sdn WHERE d='CUBA'"
cursor.execute(query_string)
# print(cursor.fetchall())
conn.close()

# PERHAPS USE THE NESTED JSON FILE. JUST HAVE ID IN ONE COLUMN AND ALL THE OTHER JSON DATA IN THE OTHER





