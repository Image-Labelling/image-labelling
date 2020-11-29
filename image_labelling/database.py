import uuid
import bcrypt
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    # id = db.Column(UUID(as_uuid=True), primary_key=True,                   default=uuid.uuid4, unique=True, nullable=False)
    id = db.Column('id', db.Unicode(128), default=lambda: str(
        uuid.uuid4()), primary_key=True)

    email = db.Column(db.Unicode(128), unique=True, nullable=False)
    username = db.Column('username', db.Unicode(128),
                         unique=True, nullable=False)
    password = db.Column(db.Unicode(128))
    password_active = db.Column(db.Boolean, unique=False, default=True)
    user_verified = db.Column(db.Boolean, unique=False, default=False)
    is_admin = db.Column(db.Boolean, unique=False, default=False)
    registration_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._authenticated = False

    def set_password(self, password):
        self.password = bcrypt.hashpw(password, self.password)

    def verify_password(self, password):
        password_hash = bcrypt.hashpw(password, self.password)
        return self.password == password_hash

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        check = self.verify_password(password)
        self._authenticated = check
        return self._authenticated


class Image(db.Model):
    __tablename__ = 'image'
    # id = db.Column(UUID(as_uuid=True), primary_key=True,                   default=uuid.uuid4, unique=True, nullable=False)
    id = db.Column('id', db.Text(length=36), default=lambda: str(
        uuid.uuid4()), primary_key=True)

    user_id = db.Column(db.Unicode(128),
                        db.ForeignKey('user.id'), nullable=True)
