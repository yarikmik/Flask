from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flaskProject.config import Config
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


#  создание flask приложения рекомендуется выполнять именно в __init__.py
def create_app():
    app = Flask(__name__)
    db.init_app(app)
    bcrypt.init_app(app)

    #  регистрация блюпринта
    from flaskProject.main.routes import main
    app.register_blueprint(main)

    #  подключаем файл конфига
    app.config.from_object(Config)

    #  регистрация логин менеджера
    login_manager.init_app(app)

    #  регистрация блюпринта пользователей
    from flaskProject.users.routes import users
    app.register_blueprint(users)

    return app
