from flask_project import db, login_manager
from datetime import datetime, timezone, timedelta
from flask_login import UserMixin
# from itsdangerous import TimedSerializer as Serializer
from authlib.jose import jwt, JoseError
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        exp = datetime.now(tz=timezone.utc) + timedelta(seconds=expires_sec)
        header = {'alg': 'HS256'}
        key = current_app.config['SECRET_KEY']
        data = {'user_id': self.id, 'exp': exp}
        return jwt.encode(header=header, payload=data, key=key)

    @staticmethod
    def verify_reset_token(token):
        key = current_app.config['SECRET_KEY']
        try:
            user_id = jwt.decode(token, key)['user_id']
            exp = jwt.decode(token, key)['exp']
            if datetime.now(tz=timezone.utc) > datetime.fromtimestamp(exp, tz=timezone.utc):
                print('JWT is now expired')
                return None
        except JoseError:
            return None
        return User.query.get(user_id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='title', lazy='dynamic')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    username = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
