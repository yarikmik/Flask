from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

#  создание flask приложения рекомендуется выполнять именно в __init__.py
def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app
