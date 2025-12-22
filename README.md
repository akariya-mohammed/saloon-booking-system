# GlamBook - Professional Hair Salon Booking System

A full-stack web application for hair salon appointment management with real-time booking, automated notifications, and comprehensive admin dashboard.

## Features

### Customer Features
- Browse available services (haircut, coloring, styling, treatments)
- Real-time availability calendar
- Online booking with instant confirmation
- Email notifications for appointments
- View and manage upcoming appointments
- Reschedule or cancel bookings

### Admin Dashboard
- Comprehensive appointment calendar (day/week/month views)
- Client management system with service history
- Service management (add/edit/remove services)
- Availability scheduling
- Appointment approval/rejection
- Revenue analytics and reporting
- Customer insights and retention metrics

### Smart Scheduling
- Automatic conflict prevention (no double-booking)
- Buffer time management between appointments
- Service duration-based scheduling
- Break time blocking
- Waitlist management for cancellations

## Tech Stack

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-JWT-Extended** - JWT authentication
- **Flask-Mail** - Email notifications
- **Flask-CORS** - Cross-origin resource sharing
- **SQLite** - Development database (PostgreSQL for production)

### Frontend
- **HTML5/CSS3** - Semantic markup and modern styling
- **JavaScript (ES6+)** - Interactive functionality
- **Bootstrap 5** - Responsive UI framework
- **FullCalendar.js** - Interactive calendar component
- **Fetch API** - RESTful API communication

### Tools & Libraries
- **Bcrypt** - Password hashing
- **python-dotenv** - Environment variable management
- **Jinja2** - Template engine

## Project Structure

```
salon-booking-system/
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── models.py             # Database models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py           # Authentication routes
│   │   ├── bookings.py       # Booking management routes
│   │   ├── services.py       # Service management routes
│   │   └── admin.py          # Admin dashboard routes
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── email.py          # Email notification helpers
│   │   └── validators.py    # Input validation
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css     # Main stylesheet
│   │   │   └── admin.css     # Admin dashboard styles
│   │   ├── js/
│   │   │   ├── booking.js    # Booking functionality
│   │   │   ├── calendar.js   # Calendar integration
│   │   │   └── admin.js      # Admin dashboard logic
│   │   └── images/           # Static images
│   └── templates/
│       ├── base.html         # Base template
│       ├── index.html        # Landing page
│       ├── booking.html      # Booking interface
│       ├── login.html        # Login page
│       └── admin/
│           ├── dashboard.html
│           ├── appointments.html
│           └── services.html
├── migrations/               # Database migrations
├── tests/                    # Unit and integration tests
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── run.py                    # Application entry point
└── .env.example              # Environment variables template
```

## Installation

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/salon-booking-system.git
cd salon-booking-system
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize database:
```bash
python run.py init-db
```

6. Run the application:
```bash
python run.py
```

Visit `http://localhost:5000` in your browser.

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new customer
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Services
- `GET /api/services` - Get all services
- `GET /api/services/<id>` - Get service details
- `POST /api/services` - Create service (admin only)
- `PUT /api/services/<id>` - Update service (admin only)
- `DELETE /api/services/<id>` - Delete service (admin only)

### Bookings
- `GET /api/bookings` - Get user bookings
- `POST /api/bookings` - Create new booking
- `GET /api/bookings/<id>` - Get booking details
- `PUT /api/bookings/<id>` - Update booking
- `DELETE /api/bookings/<id>` - Cancel booking

### Availability
- `GET /api/availability?date=YYYY-MM-DD` - Get available time slots
- `POST /api/availability` - Set availability (admin only)

### Admin
- `GET /api/admin/appointments` - Get all appointments
- `PUT /api/admin/appointments/<id>/approve` - Approve appointment
- `GET /api/admin/analytics` - Get business analytics

## Database Schema

### Users
- id (Primary Key)
- email (Unique)
- password_hash
- first_name
- last_name
- phone
- is_admin
- created_at

### Services
- id (Primary Key)
- name
- description
- duration (minutes)
- price
- image_url
- is_active

### Appointments
- id (Primary Key)
- user_id (Foreign Key → Users)
- service_id (Foreign Key → Services)
- appointment_date
- appointment_time
- status (pending/confirmed/cancelled/completed)
- notes
- created_at
- updated_at

### Availability
- id (Primary Key)
- day_of_week (0-6)
- start_time
- end_time
- is_available

## Features in Development

- [ ] SMS notifications via Twilio
- [ ] Payment integration (Stripe)
- [ ] Multi-language support
- [ ] Review and rating system
- [ ] Loyalty program
- [ ] Instagram integration for portfolio

## Testing

Run tests with:
```bash
pytest tests/
```

## Deployment

Deployed on [Render/Railway/Heroku] at: [Your deployment URL]

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

## License

MIT License

## Contact

Mohammad Akariya - [Makree29@gmail.com](mailto:Makree29@gmail.com)

Project Link: [https://github.com/akariya-mohammed/salon-booking-system](https://github.com/akariya-mohammed/salon-booking-system)
