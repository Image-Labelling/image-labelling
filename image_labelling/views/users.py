import bcrypt
from flask import Blueprint, redirect, render_template, request, flash

from image_labelling.database import User
from image_labelling.form import UserForm
from .. import db
from ..auth import admin_required

users = Blueprint('users', __name__)


@users.route('/users')
@admin_required
def show_users():
    _users = db.session.query(User)
    return render_template("users.html", users=_users)


@users.route('/register', methods=['GET', 'POST'])
def _register():
    form = UserForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            new_user.password = bcrypt.hashpw(
                new_user.password.encode('utf-8'), bcrypt.gensalt())
            db.session.add(new_user)
            db.session.commit()
            flash("Successfully registered!")
            return redirect('/')

    return render_template('register.html', form=form)
