#imports
from flask import Flask, render_template, request, json, g
import sqlite3 as sql
import testdb


app = Flask(__name__)

# functions
def query_db(query_string):
    conn = sql.connect("sdn.db")
    cursor = conn.cursor()
    cursor.execute(query_string)
    # cursor.execute("SELECT STUFF FROM STUFF")
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
def main():
    return render_template('index.html')

#new pageone
@app.route('/pageone')
def page_one():
    return render_template('page_one.html')

@app.route('/pagetwo')
def page_two():
    return render_template('page_two.html')

#execute db script?
@app.route('/exec')
def parse(name = None):
    import testdb
    print("done")
    return render_template('runDBscript.html', name = name)

@app.route('/burundi')
def show(name=None):
    sqlstring = "SELECT * FROM sdn WHERE d='BURUNDI'"
    output = query_db(sqlstring)
    #prints out html from output
    return render_template('page_two.html', output = output, name = name)


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
