from datetime import datetime

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from pinterest import db, login_manager
from flask_login import UserMixin
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User Model"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='profile_pics.jpg')
    password = db.Column(db.String(60), nullable=False)
    pins = db.relationship('Pins', backref='author', lazy=True)
    is_admin = db.Column(db.Boolean(), default=False)

    def get_reset_token(self, expires_sec=1800):
        """for generating token"""
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """for verify reset token"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User {self.username}"


class Category(db.Model, UserMixin):
    """Category Model"""
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(20), nullable=False)
    pins = db.relationship('Pins', backref='category_wise', lazy=True)


class Pins(db.Model, UserMixin):
    """Pin Model"""
    __tablename__ = 'pins'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    pin_content = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    is_private = db.Column(db.Boolean(), default=False)
    is_notification_active = db.Column(db.Boolean(), default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
