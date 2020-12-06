from .. import login_manager, db
from ..database import User
from flask import redirect, url_for

from .home import home
from .users import users
from .auth import auth
from .upload import upload

blueprints = [home, auth, users, upload]


@login_manager.user_loader
def load_user(id):
    user = db.Query.get(id)
    return user


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('auth.login'))
