from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Landing page."""
    return render_template('index.html')


@main_bp.route('/booking')
def booking():
    """Booking page."""
    return render_template('booking.html')


@main_bp.route('/login')
def login():
    """Login page."""
    return render_template('login.html')


@main_bp.route('/admin')
def admin_dashboard():
    """Admin dashboard page."""
    return render_template('admin/dashboard.html')
