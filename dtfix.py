import os
import secrets
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)

# ── Security config ───────────────────────────────────────────────────────────
# Load SECRET_KEY from environment; fall back to a random key for development
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# ── Upload config ─────────────────────────────────────────────────────────────
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_CONTENT_MB = 5

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_MB * 1024 * 1024  # 5 MB hard limit

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename: str) -> bool:
    """Return True only for whitelisted image extensions."""
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# ── Database ──────────────────────────────────────────────────────────────────
def get_db():
    """Open a connection with row_factory for cleaner access."""
    conn = sqlite3.connect("community.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS lostfound (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    name        TEXT    NOT NULL,
                    category    TEXT    NOT NULL,
                    item        TEXT    NOT NULL,
                    description TEXT    NOT NULL,
                    image       TEXT
                 )''')

    c.execute('''CREATE TABLE IF NOT EXISTS complaint (
                    id    INTEGER PRIMARY KEY AUTOINCREMENT,
                    name  TEXT NOT NULL,
                    issue TEXT NOT NULL
                 )''')

    c.execute('''CREATE TABLE IF NOT EXISTS comments (
                    id      INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER,
                    comment TEXT
                 )''')

    c.execute('''CREATE TABLE IF NOT EXISTS help (
                    id      INTEGER PRIMARY KEY AUTOINCREMENT,
                    name    TEXT NOT NULL,
                    message TEXT NOT NULL
                 )''')

    conn.commit()
    conn.close()


init_db()


# ── Helpers ───────────────────────────────────────────────────────────────────
def validate_text(value: str, max_len: int) -> str | None:
    """Strip, check non-empty, and enforce max length. Returns cleaned value or None."""
    cleaned = value.strip()[:max_len]
    return cleaned if cleaned else None


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template("home.html")


@app.route('/lostfound', methods=['GET', 'POST'])
def lostfound():
    if request.method == 'POST':
        name        = validate_text(request.form.get('name', ''),        100)
        category    = validate_text(request.form.get('category', ''),    50)
        item        = validate_text(request.form.get('item', ''),        200)
        description = validate_text(request.form.get('description', ''), 1000)

        if not all([name, category, item, description]):
            flash("All fields are required.", "error")
            return redirect(url_for('lostfound'))

        # Validate category against allowed values
        allowed_categories = {'School', 'College', 'Office', 'Hostel', 'Apartment'}
        if category not in allowed_categories:
            flash("Invalid category.", "error")
            return redirect(url_for('lostfound'))

        filename = None
        image = request.files.get('image')
        if image and image.filename:
            if not allowed_file(image.filename):
                flash("Invalid file type. Only images are allowed.", "error")
                return redirect(url_for('lostfound'))
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = get_db()
        conn.execute(
            "INSERT INTO lostfound (name, category, item, description, image) VALUES (?, ?, ?, ?, ?)",
            (name, category, item, description, filename)
        )
        conn.commit()
        conn.close()
        flash("Item posted successfully!", "success")
        return redirect(url_for('lostfound'))  # Post/Redirect/Get

    conn = get_db()
    data = conn.execute("SELECT * FROM lostfound ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("lostfound.html", data=data)


@app.route('/complaint', methods=['GET', 'POST'])
def complaint():
    if request.method == 'POST':
        name  = validate_text(request.form.get('name', ''),  100)
        issue = validate_text(request.form.get('issue', ''), 2000)

        if not name or not issue:
            flash("Both name and issue are required.", "error")
            return redirect(url_for('complaint'))

        conn = get_db()
        conn.execute("INSERT INTO complaint (name, issue) VALUES (?, ?)", (name, issue))
        conn.commit()
        conn.close()
        flash("Complaint submitted.", "success")
        return redirect(url_for('complaint'))  # Post/Redirect/Get

    conn = get_db()
    data = conn.execute("SELECT * FROM complaint ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("complaint.html", data=data)


@app.route('/help', methods=['GET', 'POST'])
def help_page():
    if request.method == 'POST':
        name    = validate_text(request.form.get('name', ''),    100)
        message = validate_text(request.form.get('message', ''), 2000)

        if not name or not message:
            flash("Both name and message are required.", "error")
            return redirect(url_for('help_page'))

        conn = get_db()
        conn.execute("INSERT INTO help (name, message) VALUES (?, ?)", (name, message))
        conn.commit()
        conn.close()
        flash("Message posted!", "success")
        return redirect(url_for('help_page'))  # Post/Redirect/Get

    conn = get_db()
    data = conn.execute("SELECT * FROM help ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("help.html", data=data)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    # debug is read from the environment; never hardcode True
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug)
