#!/usr/bin/env/python3

#imports
from flask import Flask, render_template, request, json, g, redirect

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
# def query_db(query_string):
#     conn = sql.connect("sdn.db")
#     cursor = conn.cursor()
#     cursor.execute(query_string)
#     # cursor.execute("SELECT ? FROM STUFF", stuff)
#     result = cursor.fetchall()
#     conn.close()
#     return result

def query_db(db_filename, query_string):
    conn = sql.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute(query_string)
    # cursor.execute("SELECT ? FROM STUFF", stuff)
    result = cursor.fetchall()
    conn.close()
    return result

def query_db_indiv(the_name):
    sqlstring = """
    SELECT DISTINCT * FROM sdn WHERE sdnType='individual' AND name LIKE '%{0}%'
    """.format(the_name)
    result = query_db("sdn.db", sqlstring)

    # return redirect('/final/indiv.html')
    return render_template('/final/indiv.html', result=result)

app.jinja_env.globals.update(query_db_indiv=query_db_indiv)


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

#newsfeed
@app.route('/newsfeed')
def newsfeed():
    return render_template('/final/newsfeed.html')

#newsfeed
@app.route('/orgnpage')
def orgnPage():
    return render_template('/final/orgnPage.html')

    #newsfeed
@app.route('/indivpage')
def indivPage():
    return render_template('/final/indivPage.html')

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


@app.route('/namesearch', methods=["POST"])
def make_search():
    search_category = request.form['DropDown0']
    search_term = request.form['SearchBox0']
    sqlstring = """
    SELECT DISTINCT * FROM sdn WHERE sdnType='{0}' AND name LIKE '%{1}%'
    """.format(search_category, search_term)
    result = query_db("sdn.db", sqlstring)

    return render_template('/final/indiv.html', result=result)

@app.route('/individualsearch', methods=["POST"])
def make_indiv_search():
    search_category = request.form['DropDown0']
    search_term = request.form['SearchBox0']
    location = request.form['DropDown0']
    sqlstring = """
    SELECT DISTINCT * FROM sdn WHERE sdnType='individual' AND {0} LIKE '%{1}%'
    """.format(search_category, search_term)
    result = query_db("sdn.db", sqlstring)

    return render_template('/final/indiv.html', result=result, dropdown=search_category)

@app.route('/entitysearch', methods=["POST"])
def make_entity_search():
    search_category = request.form['DropDown0']
    search_term = request.form['SearchBox0']
    sqlstring = """
    SELECT DISTINCT * FROM sdn WHERE sdnType!='individual' AND sdnType!='aircraft' AND sdnType!='entity' AND {0} LIKE '%{1}%'
    """.format(search_category, search_term)
    result = query_db("sdn.db", sqlstring)

    return render_template('/final/entity.html', result=result)

@app.route('/organizationsearch', methods=["POST"])
def make_orgn_search():
    search_term = request.form['SearchBox0']
    sqlstring = """
    SELECT DISTINCT * FROM orgs_db WHERE org_name LIKE "%{0}%"
    """.format(search_term)
    # this is vulnerable to SQL injection! Use parametrization of variables.. but then need to execute command directly... or pass in the args to the query_db function... 
    result = query_db("orgs_db.db", sqlstring)

    return render_template('/final/orgn.html', result=result)

@app.route('/aircraftsearch', methods=["POST"])
def make_aircr_search():
    search_category = request.form['DropDown0']
    search_term = request.form['SearchBox0']
    sqlstring = """
    SELECT DISTINCT * FROM sdn WHERE sdnType=='aircraft' AND {0} LIKE '%{1}%'
    """.format(search_category, search_term)
    result = query_db("sdn.db", sqlstring)

    return render_template('/final/aircr.html', result=result)

@app.route('/vesselsearch', methods=["POST"])
def make_vessel_search():
    search_category = request.form['DropDown0']
    search_term = request.form['SearchBox0']
    sqlstring = """
    SELECT DISTINCT * FROM sdn WHERE sdnType=='vessel' AND {0}  LIKE '%{1}%'
    """.format(search_category, search_term)
    result = query_db("sdn.db", sqlstring)

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


