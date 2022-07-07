from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import PrimaryKeyConstraint
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
    image_file = db.Column(db.String(200), nullable=False, default='profile_pics.jpg')
    password = db.Column(db.String(60), nullable=False)
    pins = db.relationship('Pins', backref='author', lazy='dynamic')
    is_admin = db.Column(db.Boolean(), default=False)
    pinboard = db.relationship("Pinboard", backref='pin_board', lazy='dynamic')

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
        except KeyError:
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
    image_file = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    pinboard = db.relationship("Board_of_Pins", backref='pins_in_the_board', lazy=True)
    comments = db.relationship('Comments', backref='title', lazy='dynamic')
    likes = db.relationship('Vote', backref='like', lazy='dynamic')


class Pinboard(db.Model, UserMixin):
    """Pin-board Model"""
    __tablename__ = 'pinboard'
    id = db.Column(db.Integer, primary_key=True)
    pin_board_name = db.Column(db.String(80), nullable=False)
    board_is_private = db.Column(db.Boolean())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pins = db.relationship("Board_of_Pins", backref='board_of_pins', lazy=True)


class Board_of_Pins(db.Model):
    __tablename__ = 'board_of_pins'
    __table_args__ = (
        PrimaryKeyConstraint('pin_id', 'pinboard_id'),
    )
    pin_id = db.Column(db.Integer, db.ForeignKey('pins.id'), nullable=False)
    pinboard_id = db.Column(db.Integer, db.ForeignKey('pinboard.id'), nullable=False)


class SavePin(db.Model, UserMixin):
    """Save Pins Model"""
    __tablename__ = 'savepins'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pin_id = db.Column(db.Integer, db.ForeignKey('pins.id'))


class Vote(db.Model, UserMixin):
    __tablename__ = 'vote'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pin_id = db.Column(db.Integer, db.ForeignKey('pins.id'))


class Comments(db.Model, UserMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pin_id = db.Column(db.Integer, db.ForeignKey('pins.id'))
    comment = db.Column(db.Text, nullable=False)
    date_commented = db.Column(db.DateTime(), default=datetime.utcnow)
    user = db.relationship('User', backref='user')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_name = db.Column(db.String, nullable=False)
