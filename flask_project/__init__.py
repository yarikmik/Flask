from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_project.config import Config
from flask_bcrypt import Bcrypt
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()

#  создание flask приложения рекомендуется выполнять именно в __init__.py
def create_app(config_class=Config):
    app = Flask(__name__)
    db.init_app(app)
    bcrypt.init_app(app)

    #  регистрация блюпринта
    from flask_project.main.routes import main
    app.register_blueprint(main)

    #  подключаем файл конфига
    app.config.from_object(Config)

    #  регистрация логин менеджера
    login_manager.init_app(app)

    #  регистрация блюпринта пользователей
    from flask_project.users.routes import users
    app.register_blueprint(users)

    #  регистрация блюпринта постов
    from flask_project.posts.routes import posts
    app.register_blueprint(posts)

    mail.init_app(app)

    from flask_project.errors.handlers import errors
    app.register_blueprint(errors)


    return app
