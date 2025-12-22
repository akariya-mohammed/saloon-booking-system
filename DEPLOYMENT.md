# GlamBook Deployment Guide

## Quick Start (Local Development)

1. **Clone the repository:**
```bash
git clone https://github.com/akariya-mohammed/salon-booking-system.git
cd salon-booking-system
```

2. **Create virtual environment:**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
# Copy the example file
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux

# Edit .env with your settings
```

5. **Initialize database:**
```bash
python run.py init-db
```

6. **Run the application:**
```bash
python run.py
```

Visit `http://localhost:5000` in your browser.

**Default Admin Credentials:**
- Email: `admin@glambook.com`
- Password: `admin123`

---

## Deployment to Render (Recommended)

### Prerequisites
- GitHub account
- Render account (free tier available)

### Steps

1. **Push code to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit: GlamBook salon booking system"
git branch -M main
git remote add origin https://github.com/yourusername/salon-booking-system.git
git push -u origin main
```

2. **Create Render Web Service:**
- Go to [https://render.com](https://render.com)
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Configure:
  - **Name:** glambook-app
  - **Environment:** Python 3
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `gunicorn run:app`

3. **Add Environment Variables in Render:**
```
FLASK_ENV=production
SECRET_KEY=your-production-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=postgresql://user:password@host/database
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

4. **Create PostgreSQL Database on Render:**
- Click "New +" → "PostgreSQL"
- Name: `glambook-db`
- Copy the Internal Database URL
- Add it to your Web Service as `DATABASE_URL`

5. **Initialize Production Database:**
After deployment, use Render Shell:
```bash
python run.py init-db
```

6. **Your app is live!**
Visit: `https://glambook-app.onrender.com`

---

## Deployment to Railway

1. **Install Railway CLI:**
```bash
npm install -g @railway/cli
```

2. **Login to Railway:**
```bash
railway login
```

3. **Initialize project:**
```bash
railway init
```

4. **Add PostgreSQL:**
```bash
railway add --plugin postgresql
```

5. **Set environment variables:**
```bash
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=your-secret-key
# ... add all other variables
```

6. **Deploy:**
```bash
railway up
```

---

## Deployment to Heroku

1. **Install Heroku CLI**

2. **Login:**
```bash
heroku login
```

3. **Create app:**
```bash
heroku create glambook-app
```

4. **Add PostgreSQL:**
```bash
heroku addons:create heroku-postgresql:mini
```

5. **Set environment variables:**
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key
# ... add all other variables
```

6. **Create Procfile:**
```
web: gunicorn run:app
```

7. **Deploy:**
```bash
git push heroku main
```

8. **Initialize database:**
```bash
heroku run python run.py init-db
```

---

## Post-Deployment Checklist

- [ ] Change default admin password
- [ ] Set up custom domain (optional)
- [ ] Configure email settings (Gmail App Password)
- [ ] Test all features:
  - [ ] User registration
  - [ ] Service viewing
  - [ ] Appointment booking
  - [ ] Email notifications
  - [ ] Admin dashboard
- [ ] Set up monitoring (Sentry, LogRocket)
- [ ] Configure backups for database
- [ ] Update README with live demo URL

---

## Email Configuration (Gmail)

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification
3. Generate App Password:
   - Go to "App passwords"
   - Select "Mail" and "Other"
   - Copy the generated password
   - Use it as `MAIL_PASSWORD` in your `.env`

---

## Troubleshooting

### Database Connection Issues
```bash
# Check DATABASE_URL format
postgresql://username:password@hostname:5432/database_name
```

### Email Not Sending
- Verify MAIL_USERNAME and MAIL_PASSWORD
- Check Gmail App Password is used (not regular password)
- Ensure MAIL_USE_TLS=True

### 500 Internal Server Error
```bash
# Check logs
heroku logs --tail  # For Heroku
railway logs        # For Railway
# Or check Render dashboard logs
```

---

## Maintenance

### Backup Database
```bash
# Render
pg_dump DATABASE_URL > backup.sql

# Heroku
heroku pg:backups:capture
heroku pg:backups:download
```

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

---

## Security Best Practices

1. **Never commit `.env` file**
2. **Use strong SECRET_KEY and JWT_SECRET_KEY**
3. **Change default admin password immediately**
4. **Use HTTPS in production**
5. **Enable CORS only for trusted domains**
6. **Regular security updates**

---

## Support

For issues or questions:
- Email: Makree29@gmail.com
- GitHub Issues: [https://github.com/akariya-mohammed/salon-booking-system/issues](https://github.com/akariya-mohammed/salon-booking-system/issues)
