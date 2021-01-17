import uuid
import bcrypt
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    # id = db.Column(UUID(as_uuid=True), primary_key=True,                   default=uuid.uuid4, unique=True, nullable=False)
    id = db.Column('id', db.Unicode(128), default=lambda: str(
        uuid.uuid4()), primary_key=True)

    email = db.Column(db.Unicode(128), unique=True, nullable=False)
    username = db.Column('username', db.Unicode(128),
                         unique=True, nullable=False)
    password = db.Column(db.Unicode(128))
    password_active = db.Column(db.Boolean, unique=False, default=True)
    _active = db.Column(db.Boolean, unique=False, default=False)
    _admin = db.Column(db.Boolean, unique=False, default=False)
    _anonymous = db.Column(db.Boolean, unique=False, default=False)
    registration_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._authenticated = False

    def set_password(self, password):
        self.password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(
            'utf-8'), self.password)

    # def get_id(self):
    #     return str(self.id)
    #
    # def get(self, user_id):
    #     return User.query.get(user_id)

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        check = self.verify_password(password)
        self._authenticated = check
        return self._authenticated

    @property
    def is_active(self):
        return self._active

    @property
    def is_anonymous(self):
        return self._anonymous

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Image(db.Model):
    __tablename__ = 'image'
    # id = db.Column(UUID(as_uuid=True), primary_key=True,            default=uuid.uuid4, unique=True, nullable=False)
    id = db.Column('id', db.Text(length=36), default=lambda: str(
        uuid.uuid4()), primary_key=True)
    user_id = db.Column(db.Unicode(128),
                        db.ForeignKey('user.id'), nullable=True)
    license = db.Column(db.Unicode(128), nullable=True, unique=False)
    group_id = db.Column(db.Unicode(128),
                         db.ForeignKey('image_group.id'), nullable=True)


class Segmentation(db.Model):
    __tablename__ = 'segmentation'
    id = db.Column('id', db.Text(length=36), default=lambda: str(
        uuid.uuid4()), primary_key=True)
    image_id = db.Column(db.Text(length=36),
                         db.ForeignKey('image.id'), nullable=False)
    _obscured = db.Column(db.Boolean, unique=False, default=False)
    bounding_box_x = db.Column('bounding_box_x', db.Integer(), nullable=False, unique=False)
    bounding_box_y = db.Column('bounding_box_y', db.Integer(), nullable=False, unique=False)
    bounding_box_width = db.Column('bounding_box_width', db.Integer(), nullable=False, unique=False)
    bounding_box_height = db.Column('bounding_box_height', db.Integer(), nullable=False, unique=False)


class Point(db.Model):
    __tablename__ = 'point'
    id = db.Column('id', db.Text(length=36), default=lambda: str(
        uuid.uuid4()), primary_key=True)
    segmentation_id = db.Column(db.Text(length=36), db.ForeignKey(
        'segmentation.id'), nullable=False)
    order = db.Column('order', db.Integer(), nullable=False, unique=False)
    x_coord = db.Column('x', db.Integer(), nullable=False, unique=False)
    y_coord = db.Column('y', db.Integer(), nullable=False, unique=False)


class License(db.Model):
    __tablename__ = 'license'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode(32), unique=True, nullable=False)


class Label(db.Model):
    __tablename__ = 'label'
    id = db.Column('id', db.Unicode(128), primary_key=True)
    parent_id = db.Column('parent_id', db.Unicode(128),
                          db.ForeignKey('label.id'))
    category = db.Column('category', db.Unicode(128), default='1')


class LabelEng(db.Model):
    __tablename__ = 'label_eng'
    id = db.Column('id', db.Unicode(128), primary_key=True)
    label_id = db.Column('label_id', db.Unicode(128),
                         db.ForeignKey('label.id'))
    text = db.Column('text', db.Unicode(128), nullable=False)


class LabelPol(db.Model):
    __tablename__ = 'label_pol'
    id = db.Column('id', db.Unicode(128), primary_key=True)
    label_id = db.Column('label_id', db.Unicode(128),
                         db.ForeignKey('label.id'))
    text = db.Column('text', db.Unicode(128), nullable=False)


class ImageGroup(db.Model):
    __tablename__ = 'image_group'
    id = db.Column('id', db.Unicode(128), primary_key=True)
