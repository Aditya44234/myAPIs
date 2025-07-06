from flask import Flask
from .user_system import user_bp
from .quotes_api import quotes_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    app.register_blueprint(quotes_bp)
    return app




