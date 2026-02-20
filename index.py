from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database tables
def init_db():
    conn = sqlite3.connect("community.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS lostfound
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  item TEXT,
                  description TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS complaint
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  issue TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS help
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  message TEXT)''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/lostfound', methods=['GET', 'POST'])
def lostfound():
    conn = sqlite3.connect("community.db")
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        item = request.form['item']
        description = request.form['description']

        c.execute("INSERT INTO lostfound (name, item, description) VALUES (?, ?, ?)",
                  (name, item, description))
        conn.commit()

    c.execute("SELECT * FROM lostfound")
    data = c.fetchall()
    conn.close()
    return render_template("lostfound.html", data=data)

@app.route('/complaint', methods=['GET', 'POST'])
def complaint():
    conn = sqlite3.connect("community.db")
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        issue = request.form['issue']

        c.execute("INSERT INTO complaint (name, issue) VALUES (?, ?)",
                  (name, issue))
        conn.commit()

    c.execute("SELECT * FROM complaint")
    data = c.fetchall()
    conn.close()
    return render_template("complaint.html", data=data)

@app.route('/help', methods=['GET', 'POST'])
def help_page():
    conn = sqlite3.connect("community.db")
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']

        c.execute("INSERT INTO help (name, message) VALUES (?, ?)",
                  (name, message))
        conn.commit()

    c.execute("SELECT * FROM help")
    data = c.fetchall()
    conn.close()
    return render_template("help.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)