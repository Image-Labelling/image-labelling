from .home import home
from .users import users
from .auth import auth
from .upload import upload
from .. import login_manager

blueprints = [home, auth, users, upload]


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
