from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flaskProject.config import Config

db = SQLAlchemy()
login_manager = LoginManager()


#  создание flask приложения рекомендуется выполнять именно в __init__.py
def create_app():
    app = Flask(__name__)
    db.init_app(app)

    #  регистрация блюпринта
    from flaskProject.main.routes import main
    app.register_blueprint(main)

    #  подключаем файл конфига
    app.config.from_object(Config)

    #  регистрация логин менеджера
    login_manager.init_app(app)
    return app
