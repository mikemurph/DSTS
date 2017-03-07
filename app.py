#imports
from flask import Flask, render_template, request, json, g
import sqlite3 as sql


app = Flask(__name__)

#route, handler
@app.route("/")
def main():
    return render_template('index.html')

#new pageone
@app.route('/pageone')
def page_one():
    return render_template('page_one.html')

@app.route('/pagetwo')
def page_two():
    return render_template('page_two.html')

if __name__ == "__main__":
    app.run()

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
