from flask import request, send_from_directory, Blueprint

send_file = Blueprint('sendfile', __name__)


@send_file.route('/data/<path:path>')
def sendfile(path):
    return send_from_directory('data', path)
