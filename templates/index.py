import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create database tables
def init_db():
    conn = sqlite3.connect("community.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS lostfound
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              category TEXT,
              item TEXT,
              description TEXT,
              image TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS complaint
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  issue TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS comments
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              post_id INTEGER,
              comment TEXT)''')

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
        category = request.form['category']
        item = request.form['item']
        description = request.form['description']
        image = request.files.get('image')

        filename = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        c.execute("INSERT INTO lostfound (name, category, item, description, image) VALUES (?, ?, ?, ?, ?)",
                  (name, category, item, description, filename))
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