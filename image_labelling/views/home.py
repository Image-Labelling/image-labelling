from flask import Blueprint, render_template
from flask_login import current_user

home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template("index.html", current_user=current_user)
