from flask import Blueprint, redirect, render_template, request, Flask
from image_labelling.database import db, User
from image_labelling.form import UserForm
from image_labelling.auth import admin_required


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
            db.session.add(new_user)
            db.session.commit()
            return redirect('/users')

    return render_template('register.html', form=form)