from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta, time
from app import db
from app.models import Appointment, Service, User, Availability, BlockedDate
from app.utils.email import send_booking_confirmation

bp = Blueprint('bookings', __name__, url_prefix='/api/bookings')


@bp.route('', methods=['GET'])
@jwt_required()
def get_user_bookings():
    """Get all bookings for the current user."""
    current_user_id = get_jwt_identity()
    appointments = Appointment.query.filter_by(user_id=current_user_id).order_by(Appointment.appointment_date.desc()).all()

    return jsonify({'bookings': [appointment.to_dict() for appointment in appointments]}), 200


@bp.route('/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
    """Get a specific booking."""
    current_user_id = get_jwt_identity()
    appointment = Appointment.query.get(booking_id)

    if not appointment:
        return jsonify({'error': 'Booking not found'}), 404

    # Check if user owns this booking or is admin
    user = User.query.get(current_user_id)
    if appointment.user_id != current_user_id and not user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify({'booking': appointment.to_dict()}), 200


@bp.route('', methods=['POST'])
@jwt_required()
def create_booking():
    """Create a new booking."""
    current_user_id = get_jwt_identity()
    data = request.get_json()

    # Validate required fields
    required_fields = ['service_id', 'appointment_date', 'appointment_time']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    # Validate service exists
    service = Service.query.get(data['service_id'])
    if not service or not service.is_active:
        return jsonify({'error': 'Service not found or inactive'}), 404

    # Parse date and time
    try:
        appointment_date = datetime.strptime(data['appointment_date'], '%Y-%m-%d').date()
        appointment_time = datetime.strptime(data['appointment_time'], '%H:%M').time()
    except ValueError:
        return jsonify({'error': 'Invalid date or time format'}), 400

    # Check if date is in the past
    if appointment_date < datetime.now().date():
        return jsonify({'error': 'Cannot book appointments in the past'}), 400

    # Check if date is blocked
    if BlockedDate.query.filter_by(date=appointment_date).first():
        return jsonify({'error': 'Selected date is not available'}), 400

    # Check if time slot is available
    if not is_time_slot_available(appointment_date, appointment_time, service.duration):
        return jsonify({'error': 'Selected time slot is not available'}), 409

    # Create appointment
    appointment = Appointment(
        user_id=current_user_id,
        service_id=data['service_id'],
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        notes=data.get('notes'),
        status='pending'
    )

    db.session.add(appointment)
    db.session.commit()

    # Send confirmation email
    user = User.query.get(current_user_id)
    send_booking_confirmation(user.email, appointment)

    return jsonify({
        'message': 'Booking created successfully',
        'booking': appointment.to_dict()
    }), 201


@bp.route('/<int:booking_id>', methods=['PUT'])
@jwt_required()
def update_booking(booking_id):
    """Update a booking (reschedule or add notes)."""
    current_user_id = get_jwt_identity()
    appointment = Appointment.query.get(booking_id)

    if not appointment:
        return jsonify({'error': 'Booking not found'}), 404

    # Check if user owns this booking
    if appointment.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    # Cannot update completed or cancelled appointments
    if appointment.status in ['completed', 'cancelled']:
        return jsonify({'error': f'Cannot update {appointment.status} appointments'}), 400

    data = request.get_json()

    # Update date/time if provided
    if 'appointment_date' in data or 'appointment_time' in data:
        new_date = datetime.strptime(data.get('appointment_date', appointment.appointment_date.isoformat()), '%Y-%m-%d').date()
        new_time = datetime.strptime(data.get('appointment_time', appointment.appointment_time.strftime('%H:%M')), '%H:%M').time()

        # Check if new time slot is available
        if not is_time_slot_available(new_date, new_time, appointment.service.duration, exclude_appointment_id=booking_id):
            return jsonify({'error': 'Selected time slot is not available'}), 409

        appointment.appointment_date = new_date
        appointment.appointment_time = new_time

    # Update notes if provided
    if 'notes' in data:
        appointment.notes = data['notes']

    db.session.commit()

    return jsonify({
        'message': 'Booking updated successfully',
        'booking': appointment.to_dict()
    }), 200


@bp.route('/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def cancel_booking(booking_id):
    """Cancel a booking."""
    current_user_id = get_jwt_identity()
    appointment = Appointment.query.get(booking_id)

    if not appointment:
        return jsonify({'error': 'Booking not found'}), 404

    # Check if user owns this booking
    if appointment.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    # Cannot cancel completed appointments
    if appointment.status == 'completed':
        return jsonify({'error': 'Cannot cancel completed appointments'}), 400

    appointment.status = 'cancelled'
    db.session.commit()

    return jsonify({'message': 'Booking cancelled successfully'}), 200


@bp.route('/availability', methods=['GET'])
def get_availability():
    """Get available time slots for a specific date and service."""
    date_str = request.args.get('date')
    service_id = request.args.get('service_id')

    if not date_str or not service_id:
        return jsonify({'error': 'date and service_id are required'}), 400

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    service = Service.query.get(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    available_slots = get_available_time_slots(date, service.duration)

    return jsonify({
        'date': date_str,
        'available_slots': available_slots
    }), 200


def is_time_slot_available(date, time, duration, exclude_appointment_id=None):
    """Check if a time slot is available."""
    # Check day availability
    day_of_week = date.weekday()
    availability = Availability.query.filter_by(day_of_week=day_of_week, is_available=True).first()

    if not availability:
        return False

    # Check if time is within working hours
    if time < availability.start_time or time >= availability.end_time:
        return False

    # Calculate end time of the appointment
    end_datetime = datetime.combine(date, time) + timedelta(minutes=duration)
    end_time = end_datetime.time()

    # Check for conflicting appointments
    query = Appointment.query.filter(
        Appointment.appointment_date == date,
        Appointment.status.in_(['pending', 'confirmed'])
    )

    if exclude_appointment_id:
        query = query.filter(Appointment.id != exclude_appointment_id)

    existing_appointments = query.all()

    for appt in existing_appointments:
        appt_start = appt.appointment_time
        appt_end = (datetime.combine(date, appt.appointment_time) + timedelta(minutes=appt.service.duration)).time()

        # Check for overlap
        if not (end_time <= appt_start or time >= appt_end):
            return False

    return True


def get_available_time_slots(date, duration):
    """Get all available time slots for a specific date."""
    day_of_week = date.weekday()
    availability = Availability.query.filter_by(day_of_week=day_of_week, is_available=True).first()

    if not availability:
        return []

    # Generate time slots
    slots = []
    current_time = datetime.combine(date, availability.start_time)
    end_time = datetime.combine(date, availability.end_time)

    while current_time < end_time:
        slot_time = current_time.time()
        if is_time_slot_available(date, slot_time, duration):
            slots.append(slot_time.strftime('%H:%M'))

        current_time += timedelta(minutes=30)  # 30-minute intervals

    return slots
