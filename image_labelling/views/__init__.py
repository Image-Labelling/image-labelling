from .. import login_manager, db
from ..database import User


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
    return redirect(url_for('login'))


def admin_required(func):
    @functools.wraps(func)
    def _admin_required(*args, **kw):
        admin = current_user.is_authenticated and current_user.is_admin
        if not admin:
            return app.login_manager.unauthorized()
        return func(*args, **kw)
    return _admin_required
