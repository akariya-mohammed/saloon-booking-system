from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Service, User

bp = Blueprint('services', __name__, url_prefix='/api/services')


@bp.route('', methods=['GET'])
def get_services():
    """Get all active services."""
    services = Service.query.filter_by(is_active=True).all()
    return jsonify({'services': [service.to_dict() for service in services]}), 200


@bp.route('/<int:service_id>', methods=['GET'])
def get_service(service_id):
    """Get a specific service."""
    service = Service.query.get(service_id)

    if not service:
        return jsonify({'error': 'Service not found'}), 404

    return jsonify({'service': service.to_dict()}), 200


@bp.route('', methods=['POST'])
@jwt_required()
def create_service():
    """Create a new service (admin only)."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'duration', 'price']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    service = Service(
        name=data['name'],
        description=data.get('description'),
        duration=data['duration'],
        price=data['price'],
        image_url=data.get('image_url')
    )

    db.session.add(service)
    db.session.commit()

    return jsonify({
        'message': 'Service created successfully',
        'service': service.to_dict()
    }), 201


@bp.route('/<int:service_id>', methods=['PUT'])
@jwt_required()
def update_service(service_id):
    """Update a service (admin only)."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    service = Service.query.get(service_id)

    if not service:
        return jsonify({'error': 'Service not found'}), 404

    data = request.get_json()

    # Update fields
    if 'name' in data:
        service.name = data['name']
    if 'description' in data:
        service.description = data['description']
    if 'duration' in data:
        service.duration = data['duration']
    if 'price' in data:
        service.price = data['price']
    if 'image_url' in data:
        service.image_url = data['image_url']
    if 'is_active' in data:
        service.is_active = data['is_active']

    db.session.commit()

    return jsonify({
        'message': 'Service updated successfully',
        'service': service.to_dict()
    }), 200


@bp.route('/<int:service_id>', methods=['DELETE'])
@jwt_required()
def delete_service(service_id):
    """Delete (deactivate) a service (admin only)."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    service = Service.query.get(service_id)

    if not service:
        return jsonify({'error': 'Service not found'}), 404

    # Soft delete - just deactivate
    service.is_active = False
    db.session.commit()

    return jsonify({'message': 'Service deleted successfully'}), 200
