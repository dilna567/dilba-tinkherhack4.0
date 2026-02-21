# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Python (if not already installed)
Download from [python.org](https://www.python.org/downloads/) - Python 3.7+

### 2. Clone the Project
```bash
git clone https://github.com/yourusername/dilba-tinkherhack4.0.git
cd dilba-tinkherhack4.0
```

### 3. Setup and Run
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install Flask werkzeug

# Run the app
python app.py
```

**That's it!** 🎉

### 4. Open in Browser
Go to: **http://localhost:5000**

---

## First Steps

### Sign Up
1. Click **"Sign Up"** button
2. Enter username, email, password
3. Click **"Sign Up"**
4. Login with your credentials

### Create a Post
1. Go to **Lost & Found** (after logging in)
2. Fill in the form:
   - Your name
   - Category (School, College, Office, etc.)
   - Type (Lost or Found)
   - Item name
   - Description
   - Optional: Upload image
3. Click **"Post Item"**

### File a Complaint
1. Click **"Complaints"**
2. Enter your complaint details
3. Click **"Submit Complaint"**

### Request Help
1. Click **"Help & Sharing"**
2. Describe what you need
3. Click **"Post Message"**

---

## Common Commands

```bash
# Start the app
python app.py

# Stop the app
Ctrl+C

# Reset database (start fresh)
rm community.db
python app.py

# Check Python version
python --version

# Deactivate virtual environment
deactivate
```

---

## Troubleshooting

### "Module not found" error?
```bash
pip install Flask werkzeug
```

### Port already in use?
Edit `app.py`, change line `app.run()` to `app.run(port=5001)`

### Virtual environment not activating?
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

---

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [FAQ.md](FAQ.md) for common questions
- See [DEVELOPMENT.md](DEVELOPMENT.md) for advanced setup
- Review [DEPLOYMENT.md](DEPLOYMENT.md) to deploy online

---

## Need Help?

1. Check [FAQ.md](FAQ.md)
2. Read [DEVELOPMENT.md](DEVELOPMENT.md)
3. Open an issue on GitHub
4. Contact project maintainers

---

**Happy coding!** 👨‍💻👩‍💻
