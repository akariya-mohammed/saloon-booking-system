"""Create admin user if it doesn't exist."""
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Check if admin user already exists
    admin = User.query.filter_by(email='admin@glambook.com').first()

    if admin:
        print("✅ Admin user already exists!")
        print(f"   Email: {admin.email}")
        print(f"   Name: {admin.first_name} {admin.last_name}")
    else:
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
        db.session.commit()

        print("✅ Admin user created successfully!")
        print(f"   Email: admin@glambook.com")
        print(f"   Password: admin123")
        print(f"   Please change the password after first login!")
