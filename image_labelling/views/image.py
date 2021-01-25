from flask import Blueprint, render_template, request, url_for

from ..database import Segmentation, LabelEng, db, LabelPol, Image

image = Blueprint('image', __name__)


@image.route('/image')
def show_image():
    if 'image_id' in request.args:
        _image_id = request.args.get('image_id')
        return "Fancy page that shows you stuff based on image_id."

    else:
        return "Ya need an image id, dingus."


@image.route('/image_list')
def image_list():
    if 'page' in request.args:
        _page = request.args.get('page', type=int)
        if _page < 1:
            _page = 1
    else:
        _page = 1
    uploaded_images = Image.query.order_by(Image.uploaded.desc()).paginate(page=_page, per_page=20, error_out=False)
    if uploaded_images.has_next:
        next_url = url_for('image.image_list', page=uploaded_images.next_num)
    else:
        next_url = None
    if uploaded_images.has_prev:
        prev_url = url_for('image.image_list', page=uploaded_images.prev_num)
    else:
        prev_url = None

    return render_template('image_list.html', uploaded_images=uploaded_images, next_url=next_url, prev_url=prev_url)
