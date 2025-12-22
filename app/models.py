from datetime import datetime
from app import db
import bcrypt


class User(db.Model):
    """User model for customers and admin."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    appointments = db.relationship('Appointment', backref='customer', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Verify password against hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<User {self.email}>'


class Service(db.Model):
    """Service model for salon services."""
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    appointments = db.relationship('Appointment', backref='service', lazy='dynamic')

    def to_dict(self):
        """Convert service to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'duration': self.duration,
            'price': self.price,
            'image_url': self.image_url,
            'is_active': self.is_active
        }

    def __repr__(self):
        return f'<Service {self.name}>'


class Appointment(db.Model):
    """Appointment model for bookings."""
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False, index=True)
    appointment_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='pending', index=True)  # pending, confirmed, cancelled, completed
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert appointment to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'customer_name': f"{self.customer.first_name} {self.customer.last_name}",
            'customer_email': self.customer.email,
            'customer_phone': self.customer.phone,
            'service_id': self.service_id,
            'service_name': self.service.name,
            'service_duration': self.service.duration,
            'service_price': self.service.price,
            'appointment_date': self.appointment_date.isoformat(),
            'appointment_time': self.appointment_time.strftime('%H:%M'),
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<Appointment {self.id} - {self.appointment_date} {self.appointment_time}>'


class Availability(db.Model):
    """Availability model for salon working hours."""
    __tablename__ = 'availability'

    id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.Integer, nullable=False, index=True)  # 0=Monday, 6=Sunday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert availability to dictionary."""
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return {
            'id': self.id,
            'day_of_week': self.day_of_week,
            'day_name': days[self.day_of_week],
            'start_time': self.start_time.strftime('%H:%M'),
            'end_time': self.end_time.strftime('%H:%M'),
            'is_available': self.is_available
        }

    def __repr__(self):
        return f'<Availability Day {self.day_of_week}: {self.start_time}-{self.end_time}>'


class BlockedDate(db.Model):
    """Model for blocked dates (holidays, vacations, etc.)."""
    __tablename__ = 'blocked_dates'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True, index=True)
    reason = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert blocked date to dictionary."""
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'reason': self.reason
        }

    def __repr__(self):
        return f'<BlockedDate {self.date}>'
