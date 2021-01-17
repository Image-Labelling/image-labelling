from flask import Blueprint, render_template
from flask_login import current_user

# from image_labelling.database import User
# from image_labelling.auth import current_user
# from .. import login_manager


home = Blueprint('home', __name__)


@home.route('/')
def index():
    if current_user is not None and hasattr(current_user, 'id'):
        user_id = current_user.id
    else:
        user_id = 'None'

    return render_template("index.html", current_user=current_user)
