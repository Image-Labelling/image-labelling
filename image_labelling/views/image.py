from flask import Blueprint, render_template, request, url_for

from ..database import Segmentation, LabelEng, db, LabelPol, Image

image = Blueprint('image', __name__)


@image.route('/image')
def show_image():
    if 'image_id' in request.args:
        _image_id = request.args.get('image_id')

        if 'lang' in request.args:
            lang = request.args.get('lang')
            if lang == 'pl':
                LabelTable = LabelPol
            else:
                LabelTable = LabelEng
        else:
            lang = 'en'
            LabelTable = LabelEng

        q = db.session.query(Segmentation, LabelTable) \
            .outerjoin(LabelTable, Segmentation.label_id == LabelTable.label_id) \
            .filter(Segmentation.image_id == _image_id).all()

        return render_template('image.html', image_id=_image_id, segmentations=q, lang=lang)

    else:
        return render_template('image_error.html')


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
