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

    return app
