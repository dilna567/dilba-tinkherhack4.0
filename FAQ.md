# Frequently Asked Questions (FAQ)

## Installation & Setup

### Q: What do I need to install?
**A:** You need Python 3.7+ and pip. That's it! All other dependencies are in `requirements.txt`.

### Q: How do I get started?
**A:** Follow these steps:
```bash
git clone <repo-url>
cd dilba-tinkherhack4.0
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Q: I get "ModuleNotFoundError: No module named 'flask'"
**A:** Install Flask:
```bash
pip install Flask werkzeug
```
Make sure your virtual environment is activated!

### Q: The app won't start. What's wrong?
**A:** Check:
1. Is virtual environment activated? (`source venv/bin/activate`)
2. Are dependencies installed? (`pip install -r requirements.txt`)
3. Is port 5000 available? Try changing port in `app.py`:
   ```python
   app.run(debug=True, port=5001)
   ```

---

## Usage Questions

### Q: How do I create an account?
**A:** 
1. Go to the landing page (http://localhost:5000)
2. Click "Sign Up"
3. Enter username, email, password
4. Click "Sign Up" button
5. Login with your credentials

### Q: I forgot my password. How do I reset it?
**A:** This feature is not yet implemented. You'll need to contact an administrator to reset your password in the database, or delete your account and create a new one.

### Q: How do I post a lost item?
**A:**
1. Login to your account
2. Click "Lost & Found" from home
3. Fill in the form (name, category, type, item, description)
4. Optionally upload an image
5. Click "Post Item"

### Q: What categories can I choose?
**A:** Available categories:
- School
- College
- Office
- Hostel
- Apartment

### Q: Can I delete my post?
**A:** Currently, the delete feature is not available. Please contact an admin to remove your post.

### Q: How do I upload an image?
**A:** 
1. On the form, click "Choose File" in the image section
2. Select an image from your computer
3. Supported formats: PNG, JPG, JPEG, GIF
4. Maximum size: depends on configuration (typically 5-16MB)

### Q: My image won't upload. Why?
**A:** 
- File format not supported (use PNG, JPG, JPEG, GIF)
- File size too large
- Check that `static/uploads/` directory exists

---

## Database Questions

### Q: Where is my data stored?
**A:** All data is stored in `community.db` (SQLite database) in the project root directory.

### Q: Can I export my data?
**A:** Not yet available in the UI. You can backup the database:
```bash
cp community.db community.db.backup
```

### Q: What if I want to backup my data?
**A:**
```bash
# Create a backup
cp community.db community.db.backup

# Restore from backup
cp community.db.backup community.db
```

### Q: How do I reset the database?
**A:**
```bash
# Delete the database (careful!)
rm community.db

# Restart the app - new database will be created
python app.py
```

---

## Security Questions

### Q: Is my password safe?
**A:** Yes! Passwords are encrypted using werkzeug's secure hashing algorithm.

### Q: How is the secret key used?
**A:** The secret key encrypts session data. Change it for production!

### Q: Should I change the secret key?
**A:** YES! For production deployment:
```python
# In app.py
app.secret_key = "your-new-secret-key"
```

### Q: Is the connection secure?
**A:** Currently, the app runs on HTTP (not HTTPS). For production, set up SSL/TLS certificates.

---

## Features & Roadmap

### Q: Can I see other users' profiles?
**A:** Currently, user profiles are not available. This is planned for future versions.

### Q: Can I message other users?
**A:** Not yet. Direct messaging is planned for a future release.

### Q: How do I report inappropriate content?
**A:** Currently, there's no reporting system. Please contact an administrator directly.

### Q: Can I edit my posts?
**A:** Currently, you cannot edit posts. You can only create new ones.

### Q: What features are planned?
See our [README.md - Future Enhancements](README.md#future-enhancements) section.

---

## Technical Questions

### Q: What is a virtual environment?
**A:** It's an isolated Python environment for your project. It prevents dependency conflicts:
```bash
python -m venv venv
source venv/bin/activate
```

### Q: Can I run this on Windows?
**A:** Yes! Most commands work the same, except virtual environment activation:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Q: Can I run this on a Raspberry Pi?
**A:** Yes! Install Python 3 and follow the standard setup instructions.

### Q: What Python version should I use?
**A:** Python 3.7 or higher recommended. Test with 3.11 if possible.

### Q: Can I use MySQL instead of SQLite?
**A:** Currently, the app uses SQLite. You could modify it to use MySQL, but it would require code changes.

---

## Deployment Questions

### Q: Can I deploy this to Heroku?
**A:** Yes! See [DEPLOYMENT.md](DEPLOYMENT.md#heroku) for instructions.

### Q: How do I deploy to AWS?
**A:** See [DEPLOYMENT.md](DEPLOYMENT.md#aws-ec2) for complete instructions with EC2.

### Q: Can I use a domain name?
**A:** Yes! See [SSL/HTTPS Setup](DEPLOYMENT.md#ssltls-setup) in deployment guide.

### Q: How much will hosting cost?
**A:** Depends on service:
- Free tier: Heroku Free (limited), PythonAnywhere Free
- Paid: AWS starts ~$5/month, DigitalOcean ~$5/month

### Q: How do I handle multiple users?
**A:** The app already supports multiple users with separate sessions. Scale with load balancing for production.

---

## Troubleshooting

### Q: I get "Address already in use" error
**A:**
```bash
# Another app is using port 5000
# Option 1: Change port in app.py
app.run(port=5001)

# Option 2: Find and kill the process (macOS/Linux)
lsof -i :5000
kill -9 <PID>
```

### Q: Database says "table already exists"
**A:** This is normal! It just means the tables were already created. No action needed.

### Q: Forms not submitting? 
**A:** Check:
1. Are you logged in?
2. Did you fill all required fields?
3. Check browser console for errors (F12)

### Q: CSS not loading?
**A:** 
```bash
# Check that static folder exists
ls static/
ls static/style.css
```

### Q: Images from uploads not showing?
**A:** 
```bash
# Check uploads folder exists
ls static/uploads/

# Check file permissions
chmod 755 static/uploads/
```

---

## Contributing Questions

### Q: How can I contribute?
**A:** Check [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Q: Can I fork this project?
**A:** Yes! It's open source. See [LICENSE](LICENSE) for terms.

### Q: How do I report bugs?
**A:** Create an issue on GitHub with:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)

### Q: Can I suggest new features?
**A:** Yes! Open an issue labeled "feature-request" with:
- Feature description
- Use case/benefit
- Suggested implementation (optional)

---

## Getting Help

### Where can I get more help?

1. **Documentation:** Check [README.md](README.md), [DEVELOPMENT.md](DEVELOPMENT.md)
2. **GitHub Issues:** Create an issue for bugs/questions
3. **Email:** Contact project maintainers
4. **Stack Overflow:** Tag with `flask`, `python`, `sqlite3`

### How do I report security issues?

Please email security concerns directly to the maintainers. Don't create public issues for security vulnerabilities.

---

## Still Have Questions?

1. Check the [README.md](README.md)
2. Read [DEVELOPMENT.md](DEVELOPMENT.md)
3. Review [CONFIG.md](CONFIG.md)
4. Check [DEPLOYMENT.md](DEPLOYMENT.md)
5. Open an issue on GitHub

---

Made with ❤️ at TinkerHub
