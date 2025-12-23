from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from config import config

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()


def create_app(config_name='default'):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app)

    # Register blueprints
    from app.routes import auth, bookings, services, admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(bookings.bp)
    app.register_blueprint(services.bp)
    app.register_blueprint(admin.bp)

    # Register main routes
    from app import routes
    app.register_blueprint(routes.main_bp)

    # Initialize database on first run
    with app.app_context():
        try:
            # Try to query users table - if it fails, database needs initialization
            from app.models import User
            User.query.first()
        except Exception as e:
            # Database tables don't exist, create them
            print("Initializing database tables...")
            db.create_all()

            # Create default admin user and sample data
            from app.models import Service, Availability
            import bcrypt

            # Create admin user
            admin = User(
                email='admin@glambook.com',
                first_name='Admin',
                last_name='User',
                phone='1234567890',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)

            # Create sample services
            services_data = [
                {'name': 'Women\'s Haircut', 'description': 'Professional haircut and styling', 'duration': 60, 'price': 50.00},
                {'name': 'Hair Coloring', 'description': 'Full color or highlights', 'duration': 120, 'price': 120.00},
                {'name': 'Blowout', 'description': 'Wash and professional blowout', 'duration': 45, 'price': 35.00},
                {'name': 'Deep Conditioning', 'description': 'Restorative hair treatment', 'duration': 30, 'price': 40.00},
                {'name': 'Keratin Treatment', 'description': 'Smoothing keratin treatment', 'duration': 180, 'price': 250.00},
                {'name': 'Bridal Styling', 'description': 'Wedding hair styling', 'duration': 90, 'price': 150.00}
            ]

            for service_data in services_data:
                service = Service(**service_data)
                db.session.add(service)

            # Create default availability (Monday-Saturday, 9 AM - 6 PM)
            for day in range(6):  # 0=Monday, 5=Saturday
                availability = Availability(
                    day_of_week=day,
                    start_time='09:00',
                    end_time='18:00',
                    is_available=True
                )
                db.session.add(availability)

            db.session.commit()
            print("✅ Database initialized successfully!")

    return app
