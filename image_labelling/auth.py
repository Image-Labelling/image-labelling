import functools
from flask_login import current_user, LoginManager
from image_labelling.database import User
# from flask import current_app
from . import login_manager
from flask import redirect, url_for, flash


def admin_required(func):
    @functools.wraps(func)
    def _admin_required(*args, **kw):
        admin = current_user.is_authenticated and current_user.is_admin
        if not admin:
            return login_manager.unauthorized()
        return func(*args, **kw)
    return _admin_required


@login_manager.user_loader
def load_user(_id):
    if _id is not None:
        print("User was "+_id)
        return User.query.get(_id)
    print("User was "+ _id)
    return None


@login_manager.unauthorized_handler
def unauthorized_callback():
    print("Unauthorized")
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login'))
