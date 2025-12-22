from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from sqlalchemy import func
from app import db
from app.models import Appointment, Service, User, Availability, BlockedDate

bp = Blueprint('admin', __name__, url_prefix='/api/admin')


def admin_required():
    """Decorator to check if user is admin."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return None
    return user


@bp.route('/appointments', methods=['GET'])
@jwt_required()
def get_all_appointments():
    """Get all appointments (admin only)."""
    if not admin_required():
        return jsonify({'error': 'Unauthorized'}), 403

    # Query parameters for filtering
    status = request.args.get('status')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    query = Appointment.query

    if status:
        query = query.filter_by(status=status)
    if date_from:
        query = query.filter(Appointment.appointment_date >= datetime.strptime(date_from, '%Y-%m-%d').date())
    if date_to:
        query = query.filter(Appointment.appointment_date <= datetime.strptime(date_to, '%Y-%m-%d').date())

    appointments = query.order_by(Appointment.appointment_date, Appointment.appointment_time).all()

    return jsonify({'appointments': [appointment.to_dict() for appointment in appointments]}), 200


@bp.route('/appointments/<int:appointment_id>/approve', methods=['PUT'])
@jwt_required()
def approve_appointment(appointment_id):
    """Approve a pending appointment (admin only)."""
    if not admin_required():
        return jsonify({'error': 'Unauthorized'}), 403

    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    if appointment.status != 'pending':
        return jsonify({'error': 'Only pending appointments can be approved'}), 400

    appointment.status = 'confirmed'
    db.session.commit()

    return jsonify({
        'message': 'Appointment approved successfully',
        'appointment': appointment.to_dict()
    }), 200


@bp.route('/appointments/<int:appointment_id>/reject', methods=['PUT'])
@jwt_required()
def reject_appointment(appointment_id):
    """Reject a pending appointment (admin only)."""
    if not admin_required():
        return jsonify({'error': 'Unauthorized'}), 403

    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    if appointment.status != 'pending':
        return jsonify({'error': 'Only pending appointments can be rejected'}), 400

    appointment.status = 'cancelled'
    db.session.commit()

    return jsonify({
        'message': 'Appointment rejected successfully',
        'appointment': appointment.to_dict()
    }), 200


@bp.route('/appointments/<int:appointment_id>/complete', methods=['PUT'])
@jwt_required()
def complete_appointment(appointment_id):
    """Mark an appointment as completed (admin only)."""
    if not admin_required():
        return jsonify({'error': 'Unauthorized'}), 403

    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    if appointment.status not in ['pending', 'confirmed']:
        return jsonify({'error': 'Only pending or confirmed appointments can be completed'}), 400

    appointment.status = 'completed'
    db.session.commit()

    return jsonify({
        'message': 'Appointment marked as completed',
        'appointment': appointment.to_dict()
    }), 200


@bp.route('/availability', methods=['GET'])
@jwt_required()
def get_availability():
    """Get salon availability schedule (admin only)."""
    if not admin_required():
        return jsonify({'error': 'Unauthorized'}), 403

    availability = Availability.query.order_by(Availability.day_of_week).all()

    return jsonify({'availability': [avail.to_dict() for avail in availability]}), 200


@bp.route('/availability', methods=['POST'])
@jwt_required()
def set_availability():
    """Set salon availability for a specific day (admin only)."""
    if not admin_required():
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()

    required_fields = ['day_of_week', 'start_time', 'end_time']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    # Check if availability already exists for this day
    existing = Availability.query.filter_by(day_of_week=data['day_of_week']).first()

    if existing:
        # Update existing
        existing.start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        existing.end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        existing.is_available = data.get('is_available', True)
    else:
        # Create new
        availability = Availability(
            day_of_week=data['day_of_week'],
            start_time=datetime.strptime(data['start_time'], '%H:%M').time(),
            end_time=datetime.strptime(data['end_time'], '%H:%M').time(),
            is_available=data.get('is_available', True)
        )
        db.session.add(availability)

    db.session.commit()

    return jsonify({'message': 'Availability updated successfully'}), 200


@bp.route('/blocked-dates', methods=['GET'])
@jwt_required()
def get_blocked_dates():
    """Get all blocked dates (admin only)."""
    if not admin_required():
        return jsonify({'error': 'Unauthorized'}), 403

    blocked_dates = BlockedDate.query.order_by(BlockedDate.date).all()

    return jsonify({'blocked_dates': [bd.to_dict() for bd in blocked_dates]}), 200


@bp.route('/blocked-dates', methods=['POST'])
@jwt_required()
def add_blocked_date():
    """Add a blocked date (admin only)."""
    if not admin_required():
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()

    if not data.get('date'):
        return jsonify({'error': 'date is required'}), 400

    try:
        date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    # Check if date already blocked
    if BlockedDate.query.filter_by(date=date).first():
        return jsonify({'error': 'Date already blocked'}), 409

    blocked_date = BlockedDate(
        date=date,
        reason=data.get('reason')
    )

    db.session.add(blocked_date)
    db.session.commit()

    return jsonify({
        'message': 'Date blocked successfully',
        'blocked_date': blocked_date.to_dict()
    }), 201


@bp.route('/blocked-dates/<int:blocked_date_id>', methods=['DELETE'])
@jwt_required()
def remove_blocked_date(blocked_date_id):
    """Remove a blocked date (admin only)."""
    if not admin_required():
        return jsonify({'error': 'Unauthorized'}), 403

    blocked_date = BlockedDate.query.get(blocked_date_id)

    if not blocked_date:
        return jsonify({'error': 'Blocked date not found'}), 404

    db.session.delete(blocked_date)
    db.session.commit()

    return jsonify({'message': 'Blocked date removed successfully'}), 200


@bp.route('/analytics', methods=['GET'])
@jwt_required()
def get_analytics():
    """Get business analytics (admin only)."""
    if not admin_required():
        return jsonify({'error': 'Unauthorized'}), 403

    # Get date range from query params (default: last 30 days)
    date_to = datetime.now().date()
    date_from = date_to - timedelta(days=30)

    if request.args.get('date_from'):
        date_from = datetime.strptime(request.args.get('date_from'), '%Y-%m-%d').date()
    if request.args.get('date_to'):
        date_to = datetime.strptime(request.args.get('date_to'), '%Y-%m-%d').date()

    # Total appointments
    total_appointments = Appointment.query.filter(
        Appointment.appointment_date >= date_from,
        Appointment.appointment_date <= date_to
    ).count()

    # Appointments by status
    appointments_by_status = db.session.query(
        Appointment.status,
        func.count(Appointment.id)
    ).filter(
        Appointment.appointment_date >= date_from,
        Appointment.appointment_date <= date_to
    ).group_by(Appointment.status).all()

    # Revenue from completed appointments
    revenue = db.session.query(
        func.sum(Service.price)
    ).join(Appointment).filter(
        Appointment.status == 'completed',
        Appointment.appointment_date >= date_from,
        Appointment.appointment_date <= date_to
    ).scalar() or 0

    # Most popular services
    popular_services = db.session.query(
        Service.name,
        func.count(Appointment.id).label('count')
    ).join(Appointment).filter(
        Appointment.appointment_date >= date_from,
        Appointment.appointment_date <= date_to
    ).group_by(Service.id).order_by(func.count(Appointment.id).desc()).limit(5).all()

    # Total customers
    total_customers = User.query.filter_by(is_admin=False).count()

    return jsonify({
        'date_from': date_from.isoformat(),
        'date_to': date_to.isoformat(),
        'total_appointments': total_appointments,
        'appointments_by_status': dict(appointments_by_status),
        'revenue': float(revenue),
        'popular_services': [{'name': name, 'count': count} for name, count in popular_services],
        'total_customers': total_customers
    }), 200
