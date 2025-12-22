# GlamBook - Hair Salon Booking System
## Project Summary for CV

---

## Project Overview

**GlamBook** is a professional full-stack web application designed for hair salon appointment management. The system provides real-time booking capabilities, automated email notifications, and a comprehensive admin dashboard for salon owners.

**Live Demo:** [Add your deployment URL here]
**GitHub:** https://github.com/akariya-mohammed/salon-booking-system

---

## Technical Implementation

### Architecture
- **Backend:** RESTful API built with Flask (Python)
- **Frontend:** Responsive SPA using vanilla JavaScript, HTML5, CSS3
- **Database:** SQLite (development) / PostgreSQL (production)
- **Authentication:** JWT-based token authentication
- **Email:** Flask-Mail with automated notifications

### Tech Stack

**Backend:**
- Flask 3.0 - Web framework
- SQLAlchemy - ORM for database operations
- Flask-JWT-Extended - JWT authentication & authorization
- Flask-Mail - Email notification system
- Flask-CORS - Cross-origin resource sharing
- Bcrypt - Password hashing and security

**Frontend:**
- HTML5/CSS3 - Semantic markup and modern styling
- JavaScript (ES6+) - Interactive user interface
- Bootstrap 5 - Responsive UI framework
- Font Awesome - Icon library
- Fetch API - RESTful API communication

**Database Design:**
- Users table (authentication, customer management)
- Services table (salon services catalog)
- Appointments table (booking management)
- Availability table (salon schedule)
- BlockedDates table (holidays, vacations)

**Development Tools:**
- Git - Version control
- Virtual Environment - Dependency isolation
- Gunicorn - Production WSGI server
- python-dotenv - Environment configuration

---

## Key Features Implemented

### Customer-Facing Features
✅ User registration and authentication with JWT
✅ Browse available salon services with details
✅ Real-time availability calendar
✅ Online booking with instant confirmation
✅ Email notifications for appointments
✅ View and manage upcoming appointments
✅ Reschedule or cancel bookings
✅ Responsive mobile-first design

### Admin Dashboard Features
✅ Comprehensive appointment calendar (day/week/month views)
✅ Approve/reject/complete appointment requests
✅ Client management with service history
✅ Service management (CRUD operations)
✅ Availability scheduling (set working hours)
✅ Block dates for holidays/vacations
✅ Revenue analytics and reporting
✅ Customer insights dashboard

### Smart Scheduling System
✅ Automatic conflict prevention (no double-booking)
✅ Service duration-based scheduling
✅ Buffer time management between appointments
✅ Break time blocking
✅30-minute time slot intervals
✅ Real-time availability updates

---

## API Endpoints

### Authentication (`/api/auth`)
- `POST /register` - Register new customer
- `POST /login` - User authentication
- `POST /refresh` - Refresh access token
- `GET /me` - Get current user profile
- `PUT /me` - Update user profile

### Services (`/api/services`)
- `GET /` - Get all active services
- `GET /<id>` - Get service details
- `POST /` - Create service (admin only)
- `PUT /<id>` - Update service (admin only)
- `DELETE /<id>` - Delete service (admin only)

### Bookings (`/api/bookings`)
- `GET /` - Get user bookings
- `POST /` - Create new booking
- `GET /<id>` - Get booking details
- `PUT /<id>` - Update/reschedule booking
- `DELETE /<id>` - Cancel booking
- `GET /availability` - Get available time slots

### Admin (`/api/admin`)
- `GET /appointments` - Get all appointments (with filters)
- `PUT /appointments/<id>/approve` - Approve appointment
- `PUT /appointments/<id>/reject` - Reject appointment
- `PUT /appointments/<id>/complete` - Mark as completed
- `GET /availability` - Get salon schedule
- `POST /availability` - Set availability
- `GET /blocked-dates` - Get blocked dates
- `POST /blocked-dates` - Add blocked date
- `DELETE /blocked-dates/<id>` - Remove blocked date
- `GET /analytics` - Get business analytics

---

## Challenges Solved

### 1. Conflict Prevention in Booking System
**Challenge:** Preventing double-booking and ensuring time slot availability
**Solution:** Implemented complex time slot validation algorithm that:
- Checks day-of-week availability
- Validates against working hours
- Calculates service end times with buffer
- Queries existing appointments for conflicts
- Prevents overlapping bookings

```python
def is_time_slot_available(date, time, duration, exclude_appointment_id=None):
    # Algorithm checks:
    # 1. Day availability
    # 2. Working hours
    # 3. Existing appointments
    # 4. Time overlaps with buffer
```

### 2. JWT Authentication & Authorization
**Challenge:** Secure user authentication with role-based access control
**Solution:**
- Implemented JWT token-based authentication
- Created custom decorator for admin-only routes
- Password hashing with bcrypt
- Token refresh mechanism for persistent sessions

### 3. Real-time Availability Calculation
**Challenge:** Generate available time slots dynamically based on bookings
**Solution:** Created algorithm that:
- Generates 30-minute interval slots
- Filters based on salon working hours
- Excludes already booked times
- Accounts for service duration
- Returns only available slots to frontend

### 4. Email Notification System
**Challenge:** Automated email confirmations and reminders
**Solution:**
- Integrated Flask-Mail with Gmail SMTP
- Created reusable email templates
- Implemented confirmation, reminder, and cancellation emails
- Error handling for email delivery failures

### 5. Responsive Design & UX
**Challenge:** Mobile-first design for all devices
**Solution:**
- Bootstrap 5 responsive grid system
- CSS media queries for mobile optimization
- Touch-friendly UI elements
- Progressive enhancement approach

---

## Database Schema

```sql
Users
├── id (PK)
├── email (unique, indexed)
├── password_hash
├── first_name
├── last_name
├── phone
├── is_admin
└── timestamps

Services
├── id (PK)
├── name
├── description
├── duration (minutes)
├── price
├── image_url
├── is_active
└── timestamps

Appointments
├── id (PK)
├── user_id (FK → Users)
├── service_id (FK → Services)
├── appointment_date (indexed)
├── appointment_time
├── status (indexed)
├── notes
└── timestamps

Availability
├── id (PK)
├── day_of_week (0-6, indexed)
├── start_time
├── end_time
├── is_available
└── timestamps

BlockedDates
├── id (PK)
├── date (unique, indexed)
├── reason
└── created_at
```

---

## Code Quality & Best Practices

✅ **RESTful API Design** - Standard HTTP methods and status codes
✅ **MVC Architecture** - Separation of concerns
✅ **Environment Configuration** - python-dotenv for secrets
✅ **Password Security** - Bcrypt hashing
✅ **Input Validation** - Email validation, date/time parsing
✅ **Error Handling** - Try-except blocks with meaningful messages
✅ **SQL Injection Prevention** - SQLAlchemy ORM parameterized queries
✅ **Code Documentation** - Docstrings for all functions
✅ **Git Version Control** - Proper .gitignore, meaningful commits

---

## Deployment Ready

✅ Production configuration (config.py)
✅ Gunicorn WSGI server
✅ PostgreSQL support
✅ Environment-based settings
✅ Security headers
✅ CORS configuration
✅ Deployment guides for Render, Railway, Heroku

---

## Performance Optimizations

1. **Database Indexing** - Indexed frequently queried columns (email, dates, status)
2. **Query Optimization** - Used SQLAlchemy joins to reduce N+1 queries
3. **Lazy Loading** - Dynamic relationships for better memory usage
4. **Frontend Caching** - Service data cached in browser
5. **Responsive Images** - Optimized image loading

---

## Security Features

🔒 JWT token authentication
🔒 Password hashing with bcrypt
🔒 CORS protection
🔒 Input validation and sanitization
🔒 SQL injection prevention (ORM)
🔒 XSS protection
🔒 Secure session cookies (production)
🔒 Environment variable for secrets

---

## Future Enhancements

- [ ] SMS notifications via Twilio
- [ ] Payment integration (Stripe/PayPal)
- [ ] Multi-language support (i18n)
- [ ] Review and rating system
- [ ] Loyalty rewards program
- [ ] Instagram portfolio integration
- [ ] Automated appointment reminders (cron job)
- [ ] Waitlist for cancelled appointments
- [ ] Google Calendar sync
- [ ] Mobile app (React Native)

---

## Project Statistics

- **Lines of Code:** ~2,500+
- **API Endpoints:** 20+
- **Database Tables:** 5
- **Frontend Pages:** 4
- **Development Time:** [Adjust based on when you started]
- **Tech Stack Components:** 12+

---

## How to Add to CV

### Project Title:
**GlamBook – Professional Hair Salon Booking System**

### Technologies:
Python, Flask, SQLAlchemy, JWT, PostgreSQL, JavaScript, HTML/CSS, Bootstrap, RESTful APIs

### Date:
[Month Year] – [Month Year]

### Description Bullets:

• Built full-stack salon booking system with Flask REST API, JWT authentication, and PostgreSQL database supporting real-time appointment scheduling for 100+ potential users

• Implemented complex time-slot availability algorithm preventing double-booking conflicts through automated validation of service durations, working hours, and existing appointments

• Designed RESTful API with 20+ endpoints for user authentication, booking management, and admin dashboard with role-based access control and bcrypt password security

• Created responsive mobile-first interface using Bootstrap 5 and vanilla JavaScript with real-time availability calendar and automated email notification system via Flask-Mail

• Deployed production-ready application with Gunicorn WSGI server, environment-based configuration, and comprehensive deployment guides for Render/Railway/Heroku platforms

---

## GitHub Repository Setup

1. **Create repository:**
```bash
git init
git add .
git commit -m "Initial commit: GlamBook salon booking system with Flask REST API, JWT auth, and booking management"
git branch -M main
git remote add origin https://github.com/akariya-mohammed/salon-booking-system.git
git push -u origin main
```

2. **Add README badges** (optional):
```markdown
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Flask](https://img.shields.io/badge/flask-3.0-green)
![License](https://img.shields.io/badge/license-MIT-orange)
```

---

## Demo Credentials

**Admin Access:**
- Email: admin@glambook.com
- Password: admin123

**Test Customer:**
- Create via registration page

---

## Contact & Links

**Developer:** Mohammad Akariya
**Email:** Makree29@gmail.com
**LinkedIn:** [linkedin.com/in/mohammad-akariya-185808273](https://linkedin.com/in/mohammad-akariya-185808273)
**GitHub:** [github.com/akariya-mohammed](https://github.com/akariya-mohammed)
**Portfolio:** [akariya-mohammed.github.io/html-portfolio](https://akariya-mohammed.github.io/html-portfolio)

---

**Project Repository:** https://github.com/akariya-mohammed/salon-booking-system
**Live Demo:** [Add deployment URL]
**Documentation:** See README.md and DEPLOYMENT.md

---

© 2025 Mohammad Akariya. All rights reserved.
