from flask import Flask, render_template, request, Blueprint, render_template, flash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import hashlib
import os
from flask import current_app
from flask_login import LoginManager, login_required
# from .. import login_manager
# from . import login_manager

upload = Blueprint('upload', __name__)
# login_manager=LoginManager()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in current_app.config['ALLOWED_EXTENSIONS']


@upload.route('/upload')
@login_required
def upload_file():
    return render_template('upload.html')


@upload.route('/uploader', methods=['GET', 'POST'])
def uploader_form():
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        f = request.files['file']

        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if f and allowed_file(f.filename):
            extension = f.filename.split('.')[-1]
            img_key = hashlib.sha512(f.read()).hexdigest()
            path_segment_one = img_key[0]
            path_segment_two = img_key[0:4]
            path_segment_three = img_key[4:8]

            directory_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'], path_segment_one, path_segment_two, path_segment_three)

            if not os.path.exists(directory_path):
                try:
                    os.makedirs(directory_path)
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            f.seek(0)
            f.save(os.path.join(directory_path,
                                secure_filename(img_key + '.' + extension)))
            return 'file uploaded successfully'
        else:
            return 'filetype not allowed'



