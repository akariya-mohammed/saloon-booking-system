# GlamBook - Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Setup Environment
```bash
# Navigate to project
cd salon-booking-system

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Copy example environment file
copy .env.example .env

# Minimal .env for local testing:
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key
JWT_SECRET_KEY=jwt-secret-key
```

### Step 3: Initialize Database
```bash
python run.py init-db
```

Expected output:
```
Creating database tables...
✓ Created admin user (admin@glambook.com / admin123)
✓ Created 6 sample services
✓ Created availability schedule (Mon-Sat, 9 AM - 6 PM)
✅ Database initialized successfully!
```

### Step 4: Run Application
```bash
python run.py
```

Visit: **http://localhost:5000**

---

## 🔑 Default Credentials

**Admin Login:**
- Email: `admin@glambook.com`
- Password: `admin123`

---

## 📁 Project Structure Overview

```
salon-booking-system/
│
├── app/                          # Main application package
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Database models (5 tables)
│   ├── routes/                  # API endpoints
│   │   ├── auth.py             # Authentication (register, login)
│   │   ├── bookings.py         # Booking management
│   │   ├── services.py         # Service CRUD
│   │   └── admin.py            # Admin dashboard API
│   ├── utils/
│   │   └── email.py            # Email notifications
│   ├── static/
│   │   └── css/style.css       # Custom styles
│   └── templates/               # HTML pages
│       ├── base.html
│       └── index.html
│
├── config.py                    # Configuration (dev/prod)
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
│
└── Documentation/
    ├── README.md               # Full documentation
    ├── DEPLOYMENT.md           # Deployment guides
    ├── PROJECT_SUMMARY.md      # CV summary
    └── QUICK_START.md          # This file
```

---

## 🧪 Testing the Application

### 1. Test User Registration
```bash
# Using curl
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 2. Test Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@glambook.com",
    "password": "admin123"
  }'
```

### 3. View Services (No auth required)
```bash
curl http://localhost:5000/api/services
```

### 4. Test in Browser
1. Go to http://localhost:5000
2. Click "Book Now"
3. Select a service
4. Register/Login
5. Choose date and time
6. Confirm booking

---

## 🎨 What You'll See

### Homepage
- Hero section with "Book Now" CTA
- Services grid (6 sample services)
- Features section
- Call-to-action banner

### Booking Flow
1. **Select Service** - Browse available services
2. **Choose Date** - Interactive calendar
3. **Pick Time** - Available time slots
4. **Confirm** - Review and book

### Admin Dashboard
- Appointments calendar
- Approve/reject requests
- Manage services
- Set availability
- View analytics

---

## 🛠️ Common Commands

### Database
```bash
# Initialize database
python run.py init-db

# Access Flask shell
flask shell
>>> from app.models import User
>>> User.query.all()
```

### Development
```bash
# Run with debug mode
python run.py

# Check all routes
flask routes
```

### Git
```bash
# Initialize repository
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/salon-booking-system.git
git push -u origin main
```

---

## 📧 Email Configuration (Optional)

For email notifications to work, update `.env`:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
```

**Get Gmail App Password:**
1. Go to Google Account → Security
2. Enable 2-Step Verification
3. Generate App Password
4. Copy the 16-character password
5. Use in `.env` file

---

## 🐛 Troubleshooting

### Issue: "Module not found"
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall requirements
pip install -r requirements.txt
```

### Issue: "Database locked"
```bash
# Delete database and reinitialize
del glambook.db  # Windows
rm glambook.db   # Mac/Linux

python run.py init-db
```

### Issue: "Port 5000 already in use"
```bash
# Change port in run.py (last line):
app.run(debug=True, host='0.0.0.0', port=8000)
```

### Issue: "Email not sending"
- Email feature is optional for local development
- Check spam folder
- Verify Gmail App Password (not regular password)
- For testing, you can skip email setup

---

## ✅ Checklist Before Deployment

- [ ] Change SECRET_KEY and JWT_SECRET_KEY
- [ ] Change admin password
- [ ] Set up PostgreSQL database
- [ ] Configure production email
- [ ] Set FLASK_ENV=production
- [ ] Test all API endpoints
- [ ] Update README with live URL
- [ ] Configure custom domain (optional)

---

## 📚 Next Steps

1. **Customize Branding:**
   - Update colors in `static/css/style.css`
   - Change logo and name from "GlamBook"
   - Add real service images

2. **Deploy:**
   - Follow `DEPLOYMENT.md` for Render/Railway/Heroku
   - Get live URL
   - Test in production

3. **Add to CV:**
   - Use bullets from `PROJECT_SUMMARY.md`
   - Add GitHub link
   - Add live demo link

4. **Showcase:**
   - Add to portfolio website
   - Share on LinkedIn
   - Demo in interviews

---

## 🤝 Need Help?

**Documentation:**
- Full README: `README.md`
- Deployment: `DEPLOYMENT.md`
- CV Summary: `PROJECT_SUMMARY.md`

**API Testing:**
- Use Postman/Insomnia
- Import collection from `/api/` routes
- Test with sample data

**Contact:**
- Email: Makree29@gmail.com
- GitHub: @akariya-mohammed

---

## 🎯 Project Highlights for CV

**One-Liner:**
"Full-stack salon booking system with Flask REST API, JWT authentication, and real-time scheduling"

**Key Technologies:**
Python • Flask • SQLAlchemy • PostgreSQL • JWT • JavaScript • Bootstrap • RESTful APIs

**Impact:**
- 20+ REST API endpoints
- Smart conflict-free booking algorithm
- Automated email notifications
- Role-based access control
- Production-ready deployment

---

**Happy Coding! 🚀**

Remember: This is a professional portfolio project that demonstrates:
✅ Full-stack development
✅ RESTful API design
✅ Database design & ORM
✅ Authentication & security
✅ Real-world problem solving
✅ Production deployment
