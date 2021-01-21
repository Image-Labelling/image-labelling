from flask import Blueprint, render_template, request
from flask_login import current_user

from ..database import Image
from ..database import User

profile = Blueprint('profile', __name__)


@profile.route('/profile')
def show_profile():
    if 'user_id' in request.args:
        _user_id = request.args.get('user_id', type=str)
    else:
        if current_user is not None and hasattr(current_user, 'id'):
            _user_id = current_user.id
        else:
            _user_id = '0'

    username = User.query.filter_by(id=_user_id).first().username
    upload_count = Image.query.filter_by(user_id=_user_id).count()
    uploaded_images = Image.query.filter_by(user_id=_user_id).paginate(page=1, per_page=5)

    return render_template("profile.html", username=username, upload_count=upload_count,
                           uploaded_images=uploaded_images)
