from flask import Blueprint, render_template, redirect, request, current_app, flash, abort, url_for
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from image_labelling.database import User
from image_labelling.form import LoginForm
from .. import db
from is_safe_url import is_safe_url

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email, password = form.data['email'], form.data['password']
        q = db.session.query(User).filter(User.email == email)
        user = q.first()
        if user is not None and user.authenticate(password):
            login_user(user)
            flash('Logged in successfully.')

            next = request.args.get('next')
            if next and not is_safe_url(next, allowed_hosts=request.url_root, require_https=True):
                return abort(400)
            return redirect(next or url_for('home.index'))
        # session['user_id'] = user.id
    return render_template('login.html', form=form)


@auth.route("/logout")
def logout():
    logout_user()
    # session.pop('user_id')
    return redirect('/')
