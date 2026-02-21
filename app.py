import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for login sessions

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif','pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ---------- Helper ----------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# ---------- Database ----------
def init_db():
    conn = sqlite3.connect("community.db")
    c = conn.cursor()

    # Users for login
    c.execute('''CREATE TABLE IF NOT EXISTS users(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE,
                 email TEXT UNIQUE,
                 password TEXT)''')

    # Lost & Found
    c.execute('''CREATE TABLE IF NOT EXISTS lostfound(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 category TEXT,
                 type TEXT,
                 item TEXT,
                 description TEXT,
                 image TEXT)''')

    # Complaints
    c.execute('''CREATE TABLE IF NOT EXISTS complaint(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 issue TEXT,
                 image TEXT)''')

    # Help & Sharing
    c.execute('''CREATE TABLE IF NOT EXISTS help(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 help_text TEXT,
                 share_file TEXT)''')

    conn.commit()
    conn.close()

init_db()

# ---------- Routes ----------

# Landing Page - Shows Login & Signup options
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template("index.html")

# Login Page
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect("community.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[3], password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
            return render_template("login.html")
    return render_template("login.html")

# Sign Up Page
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template("signup.html")
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return render_template("signup.html")
        
        conn = sqlite3.connect("community.db")
        c = conn.cursor()
        
        try:
            hashed_password = generate_password_hash(password)
            c.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)",
                      (username, email, hashed_password))
            conn.commit()
            flash('Account created! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists', 'error')
        finally:
            conn.close()
        
        return render_template("signup.html")
    
    return render_template("signup.html")
    
# Home Page
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template("home.html", username=session['username'])

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

# Lost & Found
@app.route('/lostfound', methods=['GET','POST'])
def lostfound():
    if 'username' not in session:
        return redirect(url_for('index'))
    conn = sqlite3.connect("community.db")
    c = conn.cursor()
    if request.method=='POST':
        name = request.form['name']
        category = request.form['category']
        type_item = request.form['type_item']  # Lost or Found
        item = request.form['item']
        description = request.form['description']
        image = request.files.get('image')

        filename = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        c.execute("INSERT INTO lostfound (name, category, type, item, description, image) VALUES (?,?,?,?,?,?)",
                  (name, category, type_item, item, description, filename))
        conn.commit()
        flash('Item posted successfully!', 'success')

    c.execute("SELECT * FROM lostfound ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return render_template("lostfound.html", data=data)

# Complaints
@app.route('/complaint', methods=['GET','POST'])
def complaint():
    if 'username' not in session:
        return redirect(url_for('index'))
    conn = sqlite3.connect("community.db")
    c = conn.cursor()
    if request.method=='POST':
        name = request.form['name']
        issue = request.form['issue']
        image = request.files.get('image')

        filename = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        c.execute("INSERT INTO complaint (name, issue, image) VALUES (?,?,?)",(name, issue, filename))
        conn.commit()
        flash('Complaint submitted!', 'success')

    c.execute("SELECT * FROM complaint ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return render_template("complaint.html", data=data)

# Help & Sharing
@app.route('/help', methods=['GET','POST'])
def help_page():
    if 'username' not in session:
        return redirect(url_for('index'))
    conn = sqlite3.connect("community.db")
    c = conn.cursor()
    if request.method=='POST':
        name = request.form['name']
        help_text = request.form['help_text']
        share_file = request.files.get('share_file')

        filename = None
        if share_file and allowed_file(share_file.filename):
            filename = secure_filename(share_file.filename)
            share_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        c.execute("INSERT INTO help (name, help_text, share_file) VALUES (?,?,?)",
                  (name, help_text, filename))
        conn.commit()
        flash('Help request posted!', 'success')

    c.execute("SELECT * FROM help ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return render_template("help.html", data=data)

if __name__=="__main__":
    app.run(debug=True)