# Deployment Guide

## Production Deployment

### Prerequisites
- Python 3.13+
- Node.js 16+ (for web)
- Server with 2GB+ RAM
- SSL certificate (for HTTPS)

### Desktop Distribution

#### Windows Installer (NSIS)
```bash
# Build installer
makensis installer.nsi

# This creates gaybeck-sms-installer.exe
```

#### Portable Version
- Just zip the `gaybeck-starkids-sms` folder
- Users can extract and run `setup.bat`

### Web Deployment

#### Option 1: Docker

```dockerfile
FROM python:3.13
WORKDIR /app
COPY web_app/backend .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

```bash
# Build and run
docker build -t gaybeck-sms .
docker run -p 5000:5000 gaybeck-sms
```

#### Option 2: Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create gaybeck-sms

# Deploy
git push heroku main
```

#### Option 3: AWS EC2

```bash
# SSH into instance
ssh -i key.pem ec2-user@your-instance

# Install Python
sudo yum install python3.13 -y

# Clone repo
git clone https://github.com/gaybeck/gaybeck-starkids-sms.git
cd gaybeck-starkids-sms

# Install and run
pip install -r requirements.txt
gunicorn -b 0.0.0.0:80 app:app
```

#### Option 4: DigitalOcean App Platform

1. Connect GitHub repository
2. Build command: `pip install -r web_app/backend/requirements.txt`
3. Run command: `python web_app/backend/app.py`
4. Port: 5000

### Frontend Deployment

#### GitHub Pages
```bash
cd web_app/frontend
npm run build

# Copy dist folder to gh-pages branch
git checkout -b gh-pages
git add dist
git commit -m "Deploy"
git push origin gh-pages
```

#### Netlify
```bash
# Connect from git
# Set build command: npm run build
# Set publish directory: dist
# Deploy!
```

#### Vercel
```bash
npm install -g vercel
vercel
# Follow prompts
```

### Database Setup (Production)

```bash
# Create backups directory
mkdir -p backups/$(date +%Y%m%d)

# Initialize database
python initialize_db.py

# Create initial backup
cp database/school_management.db backups/$(date +%Y%m%d)/backup_$(date +%H%M%S).db
```

## Environment Configuration

### Production .env
```env
# Flask
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-generate-with-secrets.token_urlsafe()

# Database
DATABASE_URL=sqlite:///database/school_management.db

# Security
JWT_SECRET_KEY=your-jwt-secret-key

# CORS
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# Session
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
```

### SSL/HTTPS Setup

```bash
# Using Let's Encrypt with Certbot
sudo certbot certonly --standalone -d yourdomain.com

# Update Nginx/Apache to use certificate
# Point to /etc/letsencrypt/live/yourdomain.com/
```

## Monitoring & Maintenance

### Health Checks
```bash
# API health
curl http://localhost:5000/api/health

# Database check
python -c "from app import app; app.app_context().push(); print('DB connected')"
```

### Automated Backups

```bash
# Cron job (Linux/Mac)
0 2 * * * /usr/local/bin/python /path/to/backup.py >> /var/log/sms-backup.log 2>&1
```

### Logging

```bash
# View Flask logs
tail -f logs/app.log

# View system logs
journalctl -u gaybeck-sms -f  # systemd
```

## Performance Optimization

### Database
- Implement database indexes on frequently queried fields
- Regular VACUUM to optimize SQLite

### API
- Enable caching for static responses
- Use CDN for static assets
- Gzip compression for responses

### Frontend
- Code splitting with Vite
- Image optimization
- Lazy loading for routes

## Security Checklist

- [ ] Change default admin password
- [ ] Enable HTTPS/SSL
- [ ] Set strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Configure CORS properly
- [ ] Enable database encryption (optional)
- [ ] Regular security updates
- [ ] Monitor error logs
- [ ] Backup database regularly
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting

## Troubleshooting

### Common Issues

**Database locked**
```bash
# Close all connections and rebuild database
rm database/school_management.db
python initialize_db.py
```

**Out of memory**
```bash
# Restart service
systemctl restart gaybeck-sms

# Or increase server RAM
```

**CORS errors**
```bash
# Check CORS_ORIGINS in .env
# Ensure frontend URL matches
```

## Support

Need help? 
- GitHub Issues: https://github.com/gaybeck/gaybeck-starkids-sms/issues
- Email: support@gaybeckstarkids.com
