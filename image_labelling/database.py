import uuid
from datetime import datetime

import bcrypt
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column('id', db.Unicode(128), default=lambda: str(
        uuid.uuid4()), primary_key=True)

    email = db.Column(db.Unicode(128), unique=True, nullable=False)
    username = db.Column('username', db.Unicode(128),
                         unique=True, nullable=False)
    password = db.Column(db.Unicode(128))
    password_active = db.Column(db.Boolean, unique=False, default=True)
    _admin = db.Column(db.Boolean, unique=False, default=False)
    registration_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def set_password(self, password):
        self.password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(
            'utf-8'), self.password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column('id', db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    user_id = db.Column('user_id', db.Unicode(128), db.ForeignKey('user.id'), nullable=True)
    license = db.Column('license_type', db.Unicode(128), nullable=True, unique=False)
    group_id = db.Column('group_id', db.Unicode(128), db.ForeignKey('image_group.id'), nullable=True)
    uploaded = db.Column('uploaded_on', db.DateTime, default=datetime.utcnow)


class Segmentation(db.Model):
    __tablename__ = 'segmentation'
    id = db.Column('id', db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    image_id = db.Column('image_id', db.Text(length=36), db.ForeignKey('image.id'), nullable=False)
    label_id = db.Column('label_id', db.Unicode(128), db.ForeignKey('label.id'), unique=False)
    _obscured = db.Column('is_obscured', db.Boolean, unique=False, default=False)
    bounding_box_x = db.Column('bounding_box_x', db.Integer(), nullable=True, unique=False)
    bounding_box_y = db.Column('bounding_box_y', db.Integer(), nullable=True, unique=False)
    bounding_box_width = db.Column('bounding_box_width', db.Integer(), nullable=True, unique=False)
    bounding_box_height = db.Column('bounding_box_height', db.Integer(), nullable=True, unique=False)


class Point(db.Model):
    __tablename__ = 'point'
    id = db.Column('id', db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    segmentation_id = db.Column('segmentation_id', db.Text(length=36), db.ForeignKey('segmentation.id'),
                                nullable=False)
    order = db.Column('order', db.Integer(), nullable=False, unique=False)
    x_coord = db.Column('x', db.Integer(), nullable=False, unique=False)
    y_coord = db.Column('y', db.Integer(), nullable=False, unique=False)

    @property
    def serialized(self):
        return {
            'order': self.order,
            'x': self.x_coord,
            'y': self.y_coord
        }


class License(db.Model):
    __tablename__ = 'license'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode(32), unique=True, nullable=False)


class Label(db.Model):
    __tablename__ = 'label'
    id = db.Column('id', db.Unicode(128), default=lambda: str(uuid.uuid4()), primary_key=True)
    parent_id = db.Column('parent_id', db.Unicode(128), db.ForeignKey('label.id'))
    category = db.Column('category', db.Unicode(128), default='1')
    segmentations = relationship("Segmentation")
    parent = relationship('Label', remote_side=id, backref='children')


class LabelEng(db.Model):
    __tablename__ = 'label_eng'
    id = db.Column('id', db.Unicode(128), default=lambda: str(uuid.uuid4()), primary_key=True)
    label_id = db.Column('label_id', db.Unicode(128),
                         db.ForeignKey('label.id'))
    text = db.Column('text', db.Unicode(128), nullable=False)


class LabelPol(db.Model):
    __tablename__ = 'label_pol'
    id = db.Column('id', db.Unicode(128), default=lambda: str(uuid.uuid4()), primary_key=True)
    label_id = db.Column('label_id', db.Unicode(128),
                         db.ForeignKey('label.id'))
    text = db.Column('text', db.Unicode(128), nullable=False)


class ImageGroup(db.Model):
    __tablename__ = 'image_group'
    id = db.Column('id', db.Unicode(128), default=lambda: str(uuid.uuid4()), primary_key=True)
    images = relationship("Image")


class VoteList(db.Model):
    __tablename__ = 'vote_list'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    segmentation_id = db.Column('segmentation_id', db.Unicode(128), db.ForeignKey('segmentation.id'), nullable=False)
    vote_power = db.Column('vote_power', db.Integer, default=0, nullable=False)
    active = db.Column('active', db.Boolean, default=False, nullable=False)


class CastVotes(db.Model):
    __tablename__ = 'cast_votes'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    vote_id = db.Column('vote_id', db.Integer, db.ForeignKey('vote_list.id'), nullable=False)
    user_id = db.Column('user_id', db.Unicode(128), db.ForeignKey('user.id'), nullable=False)
    support = db.Column('in_support', db.Boolean, nullable=False)
