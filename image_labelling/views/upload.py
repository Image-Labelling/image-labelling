import errno
import hashlib
import os

from PIL import Image as PILImage
from flask import current_app
from flask import request, Blueprint, render_template, flash, redirect, session
from werkzeug.utils import secure_filename

from ..database import Image, db

# from .. import login_manager
# from . import login_manager

upload = Blueprint('upload', __name__)

thumbnail_dir = 'thumb'
thumbnail_size = (256, 256)


# login_manager=LoginManager()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in current_app.config['ALLOWED_EXTENSIONS']


@upload.route('/upload')
# @login_required
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

            _exists = Image.query.filter_by(id=img_key).first()
            if _exists:
                return render_template('upload_error.html', error="File already uploaded before.")

            image = Image(id=img_key, user_id=session['user_id'])
            db.session.add(image)
            db.session.commit()

            directory_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'], path_segment_one, path_segment_two, path_segment_three)

            if not os.path.exists(directory_path):
                try:
                    os.makedirs(directory_path)
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            f.seek(0)
            full_file_path = os.path.join(directory_path, secure_filename(img_key))
            f.save(full_file_path)

            try:
                thumbnail_path = os.path.join(
                    current_app.config['UPLOAD_FOLDER'], thumbnail_dir, path_segment_one, path_segment_two,
                    path_segment_three)
                im = PILImage.open(full_file_path)
                im.thumbnail(thumbnail_size)
                if not os.path.exists(thumbnail_path):
                    os.makedirs(thumbnail_path)
                im.save(os.path.join(thumbnail_path, secure_filename(img_key + '.png')), "png")
            except IOError as e:
                print(repr(e))
                print("Cannot create thumbnail")

            return redirect('/image?image_id=' + img_key)
        else:
            return render_template('upload_error.html', error="Filetype not allowed.")
