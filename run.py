import os
import sys
from datetime import time
from app import create_app, db
from app.models import User, Service, Availability, Appointment, BlockedDate

app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.cli.command()
def init_db():
    """Initialize the database with tables and seed data."""
    print("Creating database tables...")
    db.create_all()

    # Create admin user
    admin = User.query.filter_by(email='admin@glambook.com').first()
    if not admin:
        admin = User(
            email='admin@glambook.com',
            first_name='Admin',
            last_name='User',
            phone='+972123456789',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        print("✓ Created admin user (admin@glambook.com / admin123)")

    # Create sample services
    services_data = [
        {
            'name': 'Classic Haircut',
            'description': 'Professional haircut with wash and blow-dry',
            'duration': 60,
            'price': 50.0,
            'image_url': '/static/images/haircut.jpg'
        },
        {
            'name': 'Hair Coloring',
            'description': 'Full hair coloring with premium products',
            'duration': 120,
            'price': 120.0,
            'image_url': '/static/images/coloring.jpg'
        },
        {
            'name': 'Balayage',
            'description': 'Hand-painted highlights for a natural look',
            'duration': 180,
            'price': 150.0,
            'image_url': '/static/images/balayage.jpg'
        },
        {
            'name': 'Hair Styling',
            'description': 'Professional styling for special occasions',
            'duration': 90,
            'price': 80.0,
            'image_url': '/static/images/styling.jpg'
        },
        {
            'name': 'Deep Conditioning Treatment',
            'description': 'Intensive moisture and repair treatment',
            'duration': 45,
            'price': 40.0,
            'image_url': '/static/images/treatment.jpg'
        },
        {
            'name': 'Keratin Treatment',
            'description': 'Smoothing treatment for frizz-free hair',
            'duration': 150,
            'price': 200.0,
            'image_url': '/static/images/keratin.jpg'
        }
    ]

    for service_data in services_data:
        if not Service.query.filter_by(name=service_data['name']).first():
            service = Service(**service_data)
            db.session.add(service)

    print(f"✓ Created {len(services_data)} sample services")

    # Create availability schedule (Monday-Saturday, 9 AM - 6 PM)
    days = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday')
    ]

    for day_num, day_name in days:
        if not Availability.query.filter_by(day_of_week=day_num).first():
            availability = Availability(
                day_of_week=day_num,
                start_time=time(9, 0),
                end_time=time(18, 0),
                is_available=True
            )
            db.session.add(availability)

    print("✓ Created availability schedule (Mon-Sat, 9 AM - 6 PM)")

    db.session.commit()
    print("\n✅ Database initialized successfully!")
    print("\nAdmin credentials:")
    print("Email: admin@glambook.com")
    print("Password: admin123")


@app.shell_context_processor
def make_shell_context():
    """Make database and models available in Flask shell."""
    return {
        'db': db,
        'User': User,
        'Service': Service,
        'Appointment': Appointment,
        'Availability': Availability,
        'BlockedDate': BlockedDate
    }


def auto_init_db():
    """Automatically initialize database on first run."""
    with app.app_context():
        try:
            # Check if tables exist
            User.query.first()
        except:
            # Tables don't exist, initialize
            print("First run detected. Initializing database...")
            init_db()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'init-db':
        with app.app_context():
            init_db()
    else:
        # Auto-initialize on first run
        auto_init_db()
        app.run(debug=True, host='0.0.0.0', port=5000)
