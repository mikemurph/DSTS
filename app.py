#!/usr/bin/env/python3

#imports
from flask import Flask, render_template, request, json, g

import sqlite3 as sql
import db_init
import feed

import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
# http://stackoverflow.com/questions/21214270/flask-run-function-every-hour
#https://pypi.python.org/pypi/schedule


app = Flask(__name__)
db_init.first_init()
db_init.db_populate()
db_init.db_pop_almanacs()


#### SCHEDULING BLOCK ####
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=db_init.db_update,
    trigger=IntervalTrigger(hours=1),
    id='updating_database',
    name='Update dabatase',
    replace_existing=True
    )
atexit.register(lambda: scheduler.shutdown())
#### END SCHEDULING BLOCK ####


# functions
def query_db(query_string):
    conn = sql.connect("sdn.db")
    cursor = conn.cursor()
    cursor.execute(query_string)
    # cursor.execute("SELECT ? FROM STUFF", stuff)
    result = cursor.fetchall()
    conn.close()
    return result


#old
#    conn = sql.connect("sdn.db")
#    cursor = conn.cursor()
#    cursor.execute(query_string)
#    # cursor.execute("SELECT STUFF FROM STUFF")
#    print(cursor.fetchall())
#    conn.close()


#route, handler
@app.route("/")
def main(debug=True):
    return render_template('/final/index.html', rows=feed.row_data)

#new pageone
@app.route('/pageone')
def page_one():
    return render_template('page_one.html')

#new pagetwo
@app.route('/pagetwo')
def page_two():
    return render_template('template/sample.html')

#new individual page
@app.route('/individual')
def individual_page():
    return render_template('/final/indiv.html')

#new individual page
@app.route('/organization')
def organization_page():
    return render_template('/final/orgn.html')

    #new individual page
@app.route('/entity')
def entity_page():
    return render_template('/final/entity.html')

#new individual page
@app.route('/aircraft')
def aircraft_page():
    return render_template('/final/aircr.html')

#new individual page
@app.route('/vessel')
def vessel_page():
    return render_template('/final/vessl.html')

#execute db script?
@app.route('/exec')
def parse(name = None):
    import db_init
    print("done")
    return render_template('runDBscript.html', name = name)

@app.route('/burundi')
def show(name=None):
    sqlstring = "SELECT * FROM sdn WHERE d='BURUNDI'"
    output = query_db(sqlstring)
    #prints out html from output
    return render_template('page_two.html', output = output, name = name)

@app.route('/namesearch', methods=["POST"])
def make_search():
    search_category = request.form['DropDown0']
    search_term = request.form['SearchBox0']
    sqlstring = """
    SELECT DISTINCT * FROM sdn WHERE sdnType='{0}' AND name LIKE '%{1}%'
    """.format(search_category, search_term) 
    result = query_db(sqlstring)

    return render_template('/final/indiv.html', result=result)

@app.route('/individualsearch', methods=["POST"])
def make_indiv_search():
    search_category = request.form['DropDown0']
    search_term = request.form['SearchBox0']
    location = request.form['DropDown0']
    sqlstring = """
    SELECT DISTINCT * FROM sdn WHERE sdnType='individual' AND {0} LIKE '%{1}%'
    """.format(search_category, search_term) 
    result = query_db(sqlstring)

    return render_template('/final/indiv.html', result=result, dropdown=search_category)

@app.route('/entitysearch', methods=["POST"])
def make_entity_search():
    search_category = request.form['DropDown0']
    search_term = request.form['SearchBox0']
    sqlstring = """
    SELECT DISTINCT * FROM sdn WHERE sdnType='entity' AND {0} LIKE '%{1}%'
    """.format(search_category, search_term) 
    result = query_db(sqlstring)

    return render_template('/final/entity.html', result=result)

@app.route('/organizationsearch', methods=["POST"])
def make_orgn_search():
    search_term = request.form['SearchBox0']
    sqlstring = """
    SELECT DISTINCT * FROM sdn WHERE sdnType!='individual' AND name LIKE '%{0}%'
    """.format(search_term) 
    result = query_db(sqlstring)

    return render_template('/final/orgn.html', result=result)

@app.route('/aircraftsearch', methods=["POST"])
def make_aircr_search():
    search_category = request.form['DropDown0']
    search_term = request.form['SearchBox0']
    sqlstring = """
    SELECT DISTINCT * FROM sdn WHERE sdnType=='aircraft' AND {0} LIKE '%{1}%'
    """.format(search_category, search_term) 
    result = query_db(sqlstring)

    return render_template('/final/aircr.html', result=result)

@app.route('/vesselsearch', methods=["POST"])
def make_vessel_search():
    search_category = request.form['DropDown0']
    search_term = request.form['SearchBox0']
    sqlstring = """
    SELECT DISTINCT * FROM sdn WHERE sdnType=='vessel' AND {0}  LIKE '%{1}%'
    """.format(search_category, search_term) 
    result = query_db(sqlstring)

    return render_template('/final/vessl.html', result=result)

# also Vessel search by flag; show countries with total count. 
# 



if __name__ == "__main__":
    app.run(debug=True)

def init_db():
    db = get_db()
    #need to create an sqlite3 database command: sqlite3 /tmp/flaskr.db < database.sql
    with app.open_resource('database.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    #initializes the database
    init_db()
    print('Initialized the database.')



# conn = sql.connect("mydatabase.db")
# cursor = conn.cursor()

# try:
#     cursor.execute("""CREATE TABLE albums
#                       (title text, artist text, release_date text,
#                        publisher text, media_type text)
#                    """)
# except:
#     pass

# cursor.execute("INSERT INTO albums VALUES ('Glow', 'Andy Hunter', '7/24/2012', 'Xplore Records', 'MP3')")
# conn.commit()
# albums = [('Exodus', 'Andy Hunter', '7/9/2002', 'Sparrow Records', 'CD'),
#           ('Until We Have Faces', 'Red', '2/1/2011', 'Essential Records', 'CD'),
#           ('The End is Where We Begin', 'Thousand Foot Krutch', '4/17/2012', 'TFKmusic', 'CD'),
#           ('The Good Life', 'Trip Lee', '4/10/2012', 'Reach Records', 'CD')]
# cursor.executemany("INSERT INTO albums VALUES (?,?,?,?,?)", albums)
# conn.commit()

# sql = "SELECT * FROM albums WHERE artist=?"
# cursor.execute(sql, [("Red")])
# print(cursor.fetchall())  # or use fetchone()

# with open('test.csv', 'r') as file:
#     dr = csv.DictReader(file)
#     to_db = [(i['title'], i['artist'], i['release_date'], i['publisher'], i['media_type']) for i in dr]
# cursor.executemany("INSERT INTO albums VALUES (?,?,?,?,?)", to_db)
# conn.commit()

# sql = "SELECT * FROM albums WHERE title='bob'"
# cursor.execute(sql)
# print(cursor.fetchall())
# conn.close()
