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

    ######
    conn = sql.connect("orgs_db.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""CREATE TABLE orgs_db 
                            (org_name text, num_desig_tot text, num_desig_ind text, num_desig_ent text, num_un_tot text, num_un_ind text, num_un_ent text)
                        """)
    except:
        pass
    conn.close()

    ######
    conn = sql.connect("natn_db.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""CREATE TABLE natn_db 
                            (nationality text, num_nation text)
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

          # print([i for i in reader])

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



def db_pop_almanacs():
    conn = sql.connect("orgs_db.db")
    cursor = conn.cursor()
    delete_string = """DELETE FROM orgs_db"""
    cursor.execute(delete_string)

    with open('almanac_orgs_static.csv', 'r') as file:
        reader = csv.DictReader(file)
        # print([i for i in reader])
        to_db = [(i['Organization'], 
            i['Number of OFAC Designations'], 
            i['Number of Individual OFAC Designations'], 
            i['Number of OFAC Entity Designations'], 
            i['Number of UN Designations'], 
            i['Number of Individual UN Designations'], 
            i['Number of Entity UN Designations']) 
            for i in reader]


    cursor.executemany("INSERT INTO orgs_db VALUES (?,?,?,?,?,?,?)", to_db)
    conn.commit()

    # query_string = "SELECT * FROM orgs_db"
    # cursor.execute(query_string)
    # print(cursor.fetchall())
    conn.close()

    ###### 

    conn = sql.connect("natn_db.db")
    cursor = conn.cursor()
    delete_string = """DELETE FROM natn_db"""
    cursor.execute(delete_string)

    with open('almanac_natn_static.csv', 'r') as file:
        reader = csv.DictReader(file)
        to_db = [(i['Nationality'], 
            i['Total OFAC Designations, by Nationality']) 
            for i in reader]


    cursor.executemany("INSERT INTO natn_db VALUES (?,?)", to_db)
    conn.commit()

    # query_string = "SELECT * FROM natn_db WHERE nationality='Afghanistan'"
    # cursor.execute(query_string)
    # # print(cursor.fetchall())
    conn.close()



