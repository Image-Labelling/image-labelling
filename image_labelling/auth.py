import functools
from flask_login import current_user, LoginManager
from image_labelling.database import User
from flask import current_app
from . import login_manager


def admin_required(func):
    @functools.wraps(func)
    def _admin_required(*args, **kw):
        admin = current_user.is_authenticated and current_user.is_admin
        if not admin:
            return login_manager.unauthorized()
        return func(*args, **kw)
    return _admin_required
