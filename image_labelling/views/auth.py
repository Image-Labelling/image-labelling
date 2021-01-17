from flask import Blueprint, render_template, redirect, request, flash, abort, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from is_safe_url import is_safe_url

from image_labelling.database import User
from image_labelling.form import LoginForm
from .. import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        email, password = form.data['email'], form.data['password']
        user = User.query.filter_by(email=email).first()

        if user is not None and user.authenticate(password):
            login_user(user, form.remember_me.data)
            print("Logged in")
            flash('Logged in successfully.')
            session['user_id'] = user.id

            next = request.args.get('next')
            if next and not is_safe_url(next, allowed_hosts=request.url_root, require_https=True):
                return abort(400)
            return redirect(next or url_for('home.index'))

    flash('Wrong username or password.')
    return render_template('login.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop('user_id')
    return redirect('/')
