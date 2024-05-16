from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app, resources={r"*": {"origins": "*"}})
    
    db.init_app(app)
    
    with app.app_context():
        from .routes import routes
        app.register_blueprint(routes)
        db.create_all()

    return app
