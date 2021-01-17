from flask import Blueprint, render_template

howto = Blueprint('howto', __name__)


@howto.route('/howto')
def how_to():
    pass
    return render_template("howto.html")
