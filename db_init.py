#imports
# from flask import Flask, render_template, request, json, g
import sqlite3 as sql
import csv
import urllib.request

def first_init():
    conn = sql.connect("sdn.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""CREATE TABLE sdn
                          (uid text, name text, sdnType text, 
                           program text, title text, callSign text, vesselType text, tonnage text, grossTonnage text, vesselFlag text, vesselOwner text, remarks text) 
                       """)
    except:
        pass
   
    conn.close()



# THIS ONE TAUGHT YOU EVERYTHING: 
# https://www.blog.pythonlibrary.org/2012/07/18/python-a-simple-step-by-step-sqlite-tutorial/


# http://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python


def db_populate():
    conn = sql.connect("sdn.db")
    cursor = conn.cursor()

    delete_string = """DELETE FROM sdn"""
    cursor.execute(delete_string)

    try:
        with open('sdn_source.csv', 'r') as file:
          reader = csv.DictReader(file)
          to_db = [(i['uid'], i['name'], i['sdnType'], i['program'], i['title'], i['callSign'], i['vesselType'], i['tonnage'], i['grossTonnage'], i['vesselFlag'], i['vesselOwner'], i['remarks']) for i in reader]
    except:
        db_update()
        with open('sdn_source.csv', 'r') as file:
          reader = csv.DictReader(file)
          to_db = [(i['uid'], i['name'], i['sdnType'], i['program'], i['title'], i['callSign'], i['vesselType'], i['tonnage'], i['grossTonnage'], i['vesselFlag'], i['vesselOwner'], i['remarks']) for i in reader]

    cursor.executemany("INSERT INTO sdn VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", to_db)
    conn.commit()

    # query_string = "SELECT * FROM sdn WHERE d='CUBA'"
    # cursor.execute(query_string)
    # print(cursor.fetchall())
    conn.close()





def db_update():
    urllib.request.urlretrieve(
        "https://www.treasury.gov/ofac/downloads/sdn.csv", 
        "sdn_source.csv"
        )

    with open('sdn_source.csv', newline='') as file:
        reader = csv.reader(file)
        data = [line for line in reader]

    with open('sdn_source.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['uid', 'name', 'sdnType', 'program', 'title', 'callSign', 'vesselType', 'tonnage', 'grossTonnage', 'vesselFlag', 'vesselOwner', 'remarks'])
        writer.writerows(data)


    db_populate()



