import datetime
import sys
from pathlib import Path
from urllib.parse import quote_plus
from flask import Flask, jsonify
from flask_migrate import Migrate
from src.extension import db
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.update(
        # JWT Configuration
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY', 'fallback-secret-key'),
        JWT_ACCESS_TOKEN_EXPIRES=datetime.timedelta(days=7),
        JWT_ALGORITHM='HS256',
        JWT_TOKEN_LOCATION=['headers'],
        
        # Database Configuration
        SQLALCHEMY_DATABASE_URI=(
            f"postgresql://{os.getenv('DB_USER')}:{quote_plus(os.getenv('DB_PASSWORD'))}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME')}"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ENGINE_OPTIONS={
            'pool_pre_ping': True,
            'pool_recycle': 3600
        }
    )

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    # JWT configuration
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "error": "Invalid token",
            "message": "Signature verification failed"
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "error": "Expired token",
            "message": "Token has expired"
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "error": "Authorization required",
            "message": "Request does not contain access token"
        }), 401

    # Register blueprints
    from src.auth import auth_blueprint
    from src.routes.api import api_blueprint
    
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify(status="ok"), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=os.getenv('FLASK_DEBUG', False))