from flask import Blueprint, redirect, render_template, request, Flask
# from image_labelling.database import User
from image_labelling.form import UserForm
# from image_labelling.auth import admin_required
from .. import db
from image_labelling.database import User
import bcrypt

users = Blueprint('users', __name__)


@users.route('/users')
def _users():
    users = db.session.query(User)
    return render_template("users.html", users=users)


@users.route('/register', methods=['GET', 'POST'])
def _register():
    form = UserForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            new_user.password = bcrypt.hashpw(new_user.password.encode('utf-8'), bcrypt.gensalt())
            db.session.add(new_user)
            db.session.commit()
            return redirect('/users')

    return render_template('register.html', form=form)
