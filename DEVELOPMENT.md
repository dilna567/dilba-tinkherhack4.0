# Development Setup Guide

## Prerequisites

- Python 3.7+
- pip (Python package manager)
- Git

## Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/dilba-tinkherhack4.0.git
cd dilba-tinkherhack4.0
```

### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
dilba-tinkherhack4.0/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── community.db          # SQLite database (auto-created)
├── README.md             # Project documentation
│
├── templates/            # HTML templates
│   ├── index.html       # Landing page
│   ├── login.html       # Login page
│   ├── signup.html      # Sign up page
│   ├── home.html        # Home dashboard
│   ├── lostfound.html   # Lost & Found page
│   ├── complaint.html   # Complaints page
│   └── help.html        # Help & Sharing page
│
└── static/              # Static files
    ├── style.css        # CSS styling
    └── uploads/         # User uploaded files
```

## Database

The SQLite database is automatically initialized on first run with these tables:

- **users**: User accounts and authentication
- **lostfound**: Lost and found item postings
- **complaint**: Community complaints
- **help**: Help requests and resource sharing

No manual database setup is required!

## Development Tips

### Adding a New Feature

1. **Update the database** (if needed):
   - Add a new `CREATE TABLE` statement in `init_db()`
   - Remember to update the database initialization code

2. **Create template** (if needed):
   - Add a new HTML file in the `templates/` directory
   - Use existing templates as reference for structure

3. **Add route** in `app.py`:
   ```python
   @app.route('/your-route', methods=['GET', 'POST'])
   def your_function():
        # Your code here
        return render_template("your-template.html")
   ```

4. **Test thoroughly**:
   - Test with valid and invalid input
   - Check authentication is working correctly
   - Verify database operations

### Common Tasks

**Reset Database:**
```bash
# Delete the database file to reset (will be recreated)
rm community.db
# or on Windows
del community.db
```

**Add a new route:**
```python
@app.route('/new-page', methods=['GET', 'POST'])
def new_page():
    # Check authentication
    if 'username' not in session:
        return redirect(url_for('index'))
    
    # Your logic here
    return render_template("new-page.html")
```

**Database operations:**
```python
# Connect to database
conn = sqlite3.connect("community.db")
c = conn.cursor()

# Execute query
c.execute("SELECT * FROM users WHERE username=?", (username,))
user = c.fetchone()

# Insert data
c.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", 
          (username, email, password))
conn.commit()

# Close connection
conn.close()
```

## Debugging

### Enable Flask Debug Mode
The app runs with `debug=True` by default, which enables:
- Auto-reloading on code changes
- Detailed error pages
- Python debugger

### Common Issues

**Port Already in Use:**
```bash
# Change the port in app.py
app.run(debug=True, port=5001)
```

**Import Errors:**
```bash
# Make sure virtual environment is activated
# Or reinstall dependencies
pip install -r requirements.txt
```

**Database Errors:**
- Delete `community.db` and restart the app
- Check file permissions on the `static/uploads/` directory

## Code Style

- Follow PEP 8 for Python
- Use meaningful variable names
- Add comments for complex logic
- Keep functions small and focused

## Testing Checklist

Before committing code:
- [ ] Application starts without errors
- [ ] Login/Signup works correctly
- [ ] All navigation links work
- [ ] Forms submit data to database
- [ ] File uploads work (if applicable)
- [ ] Session/Authentication works
- [ ] No console errors in browser

## Next Steps

- Read the [README.md](README.md) for project overview
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- Review the code structure and existing implementations

Happy coding! 🚀
