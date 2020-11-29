from flask import Blueprint, render_template

from image_labelling.database import db, User
from image_labelling.auth import current_user


home = Blueprint('home', __name__)


@home.route('/')
def index():
    if current_user is not None and hasattr(current_user, 'id'):
        user_id = current_user.id
    else:
        user_id = 'None'

    return user_id
