from flask import Blueprint, render_template, redirect, request, flash, abort, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from is_safe_url import is_safe_url

from image_labelling.database import User
from image_labelling.form import LoginForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        email, password = form.data['email'], form.data['password']
        user = User.query.filter_by(email=email).first()

        if user is not None:
            login_user(user, remember=form.remember_me.data)
            print("Logged in")
            flash('Logged in successfully.')
            session['user_id'] = user.id
            session['logged_in'] = True

            _next = request.args.get('next')
            if _next and not is_safe_url(_next, allowed_hosts=request.url_root, require_https=True):
                return abort(400)
            return redirect(_next or url_for('home.index'))

    flash('Wrong username or password.')
    return render_template('login.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop('user_id')
    session['logged_in'] = False
    return redirect('/')
