from .. import login_manager, db
from flask import redirect, url_for

from .home import home
from .users import users
from .auth import auth
from .upload import upload
from .label import label
from .create_polygon import create_polygon
from .send_files import send_file
from .howto import howto
from .profile import profile
from .image import image

blueprints = [home, auth, users, upload, label, create_polygon, send_file, howto, profile, image]

# @login_manager.user_loader
# def load_user(_id):
#     user = db.Query.get(_id)
#     return user
#
#
# @login_manager.unauthorized_handler
# def unauthorized_callback():
#     print("Unauthorized")
#     return redirect(url_for('auth.login'))
