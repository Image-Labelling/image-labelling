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

    def get_id(self):
        return self.id

    def get(user_id):
        return User.query.get(id)

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
    # id = db.Column(UUID(as_uuid=True), primary_key=True,                   default=uuid.uuid4, unique=True, nullable=False)
    id = db.Column('id', db.Text(length=36), default=lambda: str(
        uuid.uuid4()), primary_key=True)

    user_id = db.Column(db.Unicode(128),
                        db.ForeignKey('user.id'), nullable=True)
