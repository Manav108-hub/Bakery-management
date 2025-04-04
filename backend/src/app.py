import datetime
import sys
from pathlib import Path
from urllib.parse import quote_plus
from flask import Flask
from src.extension import db
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # URL encode password
    encoded_password = quote_plus(os.getenv('DB_PASSWORD'))

    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=7)
    jwt = JWTManager(app)
    
    # Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.getenv('DB_USER')}:{encoded_password}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    with app.app_context():
        from src.auth import auth_blueprint
        from src.routes.api import api_blueprint
        
        app.register_blueprint(auth_blueprint, url_prefix='/auth')
        app.register_blueprint(api_blueprint, url_prefix='/api')
        
        # Create tables if they don't exist
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000)