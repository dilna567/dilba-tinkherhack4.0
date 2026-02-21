# Configuration Guide

## Environment Configuration

### Secret Key
The application uses a secret key for session management. Change this in production!

```python
# app.py
app.secret_key = "your-secret-key-here"
```

**In Production:**
```python
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-key')
```

## Flask Configuration

### Debug Mode
```python
# Enable debug mode (only in development!)
app.run(debug=True)

# Disable for production
app.run(debug=False)
```

### Port Configuration
```python
# Default: localhost:5000
app.run(port=5000)

# Custom port
app.run(port=8000)
```

## File Upload Configuration

### Upload Folder
```python
UPLOAD_FOLDER = 'static/uploads'
```

### Allowed File Extensions
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
```

To add more extensions:
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'xlsx'}
```

### Maximum File Size
```python
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
```

## Database Configuration

### Database File Location
```python
DATABASE = "community.db"  # Current directory
# or
DATABASE = "/var/lib/app/community.db"  # Production path
```

### Database Backup
To backup your database:
```bash
cp community.db community.db.backup
```

## Security Configuration

### Update Secret Key (Important for Production!)
```bash
# Generate a random secret key
python -c "import secrets; print(secrets.token_hex(32))"
```

### Set Environment Variable
```bash
# On Windows (PowerShell)
$env:SECRET_KEY = "your-generated-key"

# On macOS/Linux
export SECRET_KEY="your-generated-key"
```

Update app.py:
```python
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
```

## Password Configuration

### Minimum Password Length
Currently set to 6 characters. To change:

In `signup()` function in app.py:
```python
if len(password) < 8:  # Change 8 to desired length
    flash('Password must be at least 8 characters', 'error')
```

## CORS Configuration (if needed)

To enable CORS for API access:
```bash
pip install flask-cors
```

```python
from flask_cors import CORS

CORS(app)
```

## Error Handling

### Enable Detailed Error Pages (Development Only)
```python
app.config['TRAP_HTTP_EXCEPTIONS'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
```

### Set Custom Error Handlers
```python
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500
```

## Logging Configuration

Add logging for better debugging:

```python
import logging

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Use in your code
@app.route('/login', methods=['POST'])
def login():
    app.logger.info(f"Login attempt for user: {username}")
```

## Email Configuration (for future features)

Example setup for sending emails:

```python
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')

mail = Mail(app)
```

## Session Configuration

### Session Timeout
```python
from datetime import timedelta

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JavaScript access
```

## Database Connection Pooling

For better performance with multiple requests:

```python
import sqlite3
from contextlib import contextmanager

DATABASE = "community.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE)
    try:
        yield conn
    finally:
        conn.close()
```

## Performance Optimization

### Enable Query Caching
```python
app.config['SQLALCHEMY_ECHO'] = False  # Disable query logging for production
```

### Enable Compression
```bash
pip install flask-compress
```

```python
from flask_compress import Compress
Compress(app)
```

## Production Deployment Configuration

```python
# Production settings
DEBUG = False
TESTING = False
ENV = 'production'

# Security settings
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Server
PREFERRED_URL_SCHEME = 'https'
```

## Starting the Application

### Development
```bash
python app.py
```

### Production (with Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Production (with uWSGI)
```bash
pip install uwsgi
uwsgi --http :5000 --wsgi-file app.py --callable app
```

---

For more Flask configuration options, refer to the [Flask Configuration Documentation](https://flask.palletsprojects.com/config/)
