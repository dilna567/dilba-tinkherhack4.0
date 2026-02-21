# Deployment Guide

## Local Deployment

### Prerequisites
- Python 3.7+
- pip
- Virtual environment

### Steps

1. **Clone and Setup**
```bash
git clone https://github.com/yourusername/dilba-tinkherhack4.0.git
cd dilba-tinkherhack4.0
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Update Configuration**
Edit `app.py`:
```python
app.secret_key = "your-secure-secret-key"
app.run(debug=False, host='0.0.0.0', port=5000)
```

3. **Run Application**
```bash
python app.py
```

4. **Access Application**
Open browser: `http://localhost:5000`

---

## Cloud Deployment

### Heroku

**Prerequisites:**
- Heroku account
- Heroku CLI installed

**Steps:**

1. **Create Heroku App**
```bash
heroku create your-app-name
```

2. **Create Procfile**
```
web: gunicorn app:app
```

3. **Create runtime.txt**
```
python-3.11.0
```

4. **Update requirements.txt**
```bash
pip install gunicorn
pip freeze > requirements.txt
```

5. **Deploy**
```bash
heroku login
git push heroku main
```

6. **View Logs**
```bash
heroku logs --tail
```

### PythonAnywhere

**Steps:**

1. **Sign up** at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload Files**
- Upload your project files via web interface

3. **Create Virtual Environment**
```bash
mkvirtualenv --python=/usr/bin/python3.11 myapp
pip install flask werkzeug
```

4. **Create Web App**
- Go to Web tab
- Add new web app
- Choose Flask framework

5. **Configure WSGI**
Edit the WSGI configuration file:
```python
import sys
path = '/home/yourusername/myapp'
if path not in sys.path:
    sys.path.insert(0, path)

from app import app as application
```

6. **Restart Web App**

### AWS EC2

**Prerequisites:**
- AWS account
- EC2 instance running Ubuntu 20.04

**Steps:**

1. **SSH into Instance**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

2. **Install Python and Dependencies**
```bash
sudo apt update
sudo apt install python3-pip python3-venv
```

3. **Clone Repository**
```bash
git clone https://github.com/yourusername/dilba-tinkherhack4.0.git
cd dilba-tinkherhack4.0
```

4. **Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

5. **Create Systemd Service**
Create `/etc/systemd/system/dilba.service`:
```ini
[Unit]
Description=Dilba Community Platform
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/dilba-tinkherhack4.0
Environment="PATH=/home/ubuntu/dilba-tinkherhack4.0/venv/bin"
ExecStart=/home/ubuntu/dilba-tinkherhack4.0/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

6. **Enable and Start Service**
```bash
sudo systemctl enable dilba
sudo systemctl start dilba
```

7. **Setup Nginx Reverse Proxy**
```bash
sudo apt install nginx
```

Create `/etc/nginx/sites-available/dilba`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /home/ubuntu/dilba-tinkherhack4.0/static;
    }
}
```

8. **Enable Site**
```bash
sudo ln -s /etc/nginx/sites-available/dilba /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Google Cloud Run

**Prerequisites:**
- Google Cloud account
- gcloud CLI

**Steps:**

1. **Create Dockerfile**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD exec gunicorn --bind :$PORT --workers 1 --timeout 0 app:app
```

2. **Build and Deploy**
```bash
gcloud builds submit --tag gcr.io/your-project/dilba
gcloud run deploy dilba --image gcr.io/your-project/dilba --platform managed
```

### Docker Deployment

**Create Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create uploads directory
RUN mkdir -p static/uploads

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

**Build and Run**
```bash
docker build -t community-platform .
docker run -p 5000:5000 community-platform
```

---

## SSL/HTTPS Setup

### Let's Encrypt with Certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com
```

Update Nginx configuration to use SSL:
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # ... rest of configuration
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

---

## Database Management

### Backup Database
```bash
cp community.db community.db.backup
```

### Restore Database
```bash
cp community.db.backup community.db
```

### Remote Database (Optional)

For production, consider using a hosted database service like:
- MySQL/PostgreSQL on AWS RDS
- MongoDB Atlas
- Google Cloud SQL

Update connection string in `app.py` accordingly.

---

## Monitoring and Maintenance

### Monitor Application
```bash
# If using systemd
sudo journalctl -u dilba -f

# Check Flask logs
tail -f app.log
```

### Backup Schedule
Create a cron job for automatic backups:
```bash
# Backup daily at 2 AM
0 2 * * * cp /path/to/community.db /mnt/backup/community.db.$(date +\%Y\%m\%d)
```

### Update Application
```bash
cd /path/to/app
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart dilba
```

---

## Troubleshooting

### Port in Use
```bash
# Find process using port 5000
lsof -i :5000
# Kill process
kill -9 <PID>
```

### Permission Denied
```bash
# Fix file permissions
chmod -R 755 static/
chmod -R 755 static/uploads/
```

### Database Locked
```bash
# Remove lock file if it exists
rm community.db-journal
```

---

## Performance Optimization

1. **Enable Caching**
   - Use Redis for session storage
   - Cache static files

2. **Database Optimization**
   - Add indexes on frequently queried columns
   - Regular database maintenance

3. **Load Balancing**
   - Use multiple Gunicorn workers
   - Deploy behind a load balancer

4. **CDN**
   - Serve static files from CDN
   - Reduces server load

---

## Security Checklist

- [ ] Update Flask secret key for production
- [ ] Enable HTTPS/SSL
- [ ] Set up firewall rules
- [ ] Configure environment variables properly
- [ ] Enable CORS only for trusted domains
- [ ] Regular security updates
- [ ] Set up automated backups
- [ ] Monitor access logs
- [ ] Use strong database passwords
- [ ] Keep dependencies updated

---

For more information, refer to [Flask Deployment Documentation](https://flask.palletsprojects.com/deployment/)
