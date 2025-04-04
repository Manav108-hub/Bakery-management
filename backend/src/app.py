from urllib.parse import quote_plus
from flask import Flask
from src.extension import db
from dotenv import load_dotenv
import os

# Load environment variables (only once is needed)
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # URL encode the DB password to handle special characters
    encoded_password = quote_plus(os.getenv('DB_PASSWORD'))
    
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.getenv('DB_USER')}:{encoded_password}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    print("DATABASE URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    
    # Import and register blueprints
    with app.app_context():
        from src.routes.api import api_blueprint
        app.register_blueprint(api_blueprint, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000)
