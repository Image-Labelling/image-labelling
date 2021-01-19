from flask import Blueprint, redirect, render_template, request, flash

from flask_login import current_user

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

    return _user_id
