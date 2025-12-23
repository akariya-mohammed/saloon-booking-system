from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from config import config
from datetime import time

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
            from app.models import User, Service, Availability

            # Check if tables exist
            User.query.first()

            # Check if we need to seed services
            if Service.query.count() == 0:
                print("No services found. Seeding services...")

                services_data = [
                    {'name': 'Women\'s Haircut', 'description': 'Professional haircut and styling', 'duration': 60, 'price': 50.00, 'is_active': True},
                    {'name': 'Hair Coloring', 'description': 'Full color or highlights', 'duration': 120, 'price': 120.00, 'is_active': True},
                    {'name': 'Blowout', 'description': 'Wash and professional blowout', 'duration': 45, 'price': 35.00, 'is_active': True},
                    {'name': 'Deep Conditioning', 'description': 'Restorative hair treatment', 'duration': 30, 'price': 40.00, 'is_active': True},
                    {'name': 'Keratin Treatment', 'description': 'Smoothing keratin treatment', 'duration': 180, 'price': 250.00, 'is_active': True},
                    {'name': 'Bridal Styling', 'description': 'Wedding hair styling', 'duration': 90, 'price': 150.00, 'is_active': True}
                ]

                for service_data in services_data:
                    service = Service(**service_data)
                    db.session.add(service)

                db.session.commit()
                print("✅ Services seeded successfully!")

            # Check if we need to seed availability
            if Availability.query.count() == 0:
                print("No availability found. Seeding availability...")

                # Create default availability (Monday-Saturday, 9 AM - 6 PM)
                for day in range(6):  # 0=Monday, 5=Saturday
                    availability = Availability(
                        day_of_week=day,
                        start_time=time(9, 0),  # 9:00 AM
                        end_time=time(18, 0),   # 6:00 PM
                        is_available=True
                    )
                    db.session.add(availability)

                db.session.commit()
                print("✅ Availability seeded successfully!")

        except Exception as e:
            # Database tables don't exist, create them
            print("Initializing database tables...")

            # Rollback any failed transaction
            db.session.rollback()

            # Create all tables
            db.create_all()

            # Create default admin user and sample data
            from app.models import Service, Availability

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
                {'name': 'Women\'s Haircut', 'description': 'Professional haircut and styling', 'duration': 60, 'price': 50.00, 'is_active': True},
                {'name': 'Hair Coloring', 'description': 'Full color or highlights', 'duration': 120, 'price': 120.00, 'is_active': True},
                {'name': 'Blowout', 'description': 'Wash and professional blowout', 'duration': 45, 'price': 35.00, 'is_active': True},
                {'name': 'Deep Conditioning', 'description': 'Restorative hair treatment', 'duration': 30, 'price': 40.00, 'is_active': True},
                {'name': 'Keratin Treatment', 'description': 'Smoothing keratin treatment', 'duration': 180, 'price': 250.00, 'is_active': True},
                {'name': 'Bridal Styling', 'description': 'Wedding hair styling', 'duration': 90, 'price': 150.00, 'is_active': True}
            ]

            for service_data in services_data:
                service = Service(**service_data)
                db.session.add(service)

            # Create default availability (Monday-Saturday, 9 AM - 6 PM)
            for day in range(6):  # 0=Monday, 5=Saturday
                availability = Availability(
                    day_of_week=day,
                    start_time=time(9, 0),  # 9:00 AM
                    end_time=time(18, 0),   # 6:00 PM
                    is_available=True
                )
                db.session.add(availability)

            try:
                db.session.commit()
                print("✅ Database initialized successfully!")
            except Exception as commit_error:
                db.session.rollback()
                print(f"❌ Database initialization failed: {commit_error}")

    return app
