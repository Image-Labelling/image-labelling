from flask import request, Blueprint, render_template, redirect, url_for, flash

from image_labelling.database import Label, db, LabelEng, LabelPol
from image_labelling.form import LabelForm, LabelAssignForm
from ..database import Segmentation

label = Blueprint('label', __name__)


@label.route("/label", methods=['GET', 'POST'])
def add_label():
    form = LabelForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():

        parent = request.form['parent']
        name = request.form['name']
        language = request.form['language']

        new_label = Label()
        if language == 'English':
            _label = LabelEng()
            if parent is not None:
                _parent_id = LabelEng.query.filter_by(text=parent).first()

        if language == 'Polish':
            _label = LabelPol()
            if parent is not None:
                _parent_id = LabelPol.query.filter_by(text=parent).first()

        if _parent_id is not None:
            new_label.parent_id = _parent_id.label_id

        db.session.add(new_label)
        db.session.commit()

        _label.label_id = new_label.id

        _label.text = name

        db.session.add(_label)
        db.session.commit()

        flash("Label added successfully.")
        return redirect('/label')

    return render_template('label.html', form=form)


@label.route('/label_change')
def label_change():
    if 'segmentation_id' not in request.args:
        return 'Malformed request'

    if 'vote' in request.args and request.args.get('vote') == 'yes':
        return 'Vote'
    if 'create_new' in request.args and request.args.get('create_new') == 'yes':
        return 'Make new'

    return '500 BAD PATH'


@label.route('/label_assign', methods=['GET', 'POST'])
def label_assign():
    form = LabelAssignForm(request.form)
    if 'segmentation_id' in request.args:
        _segmentation_id = request.args.get('segmentation_id')
        if request.method == 'POST' and form.validate_on_submit():

            name = request.form['name']
            language = request.form['language']

            _segmentation = Segmentation.query.filter_by(id=_segmentation_id).first()
            if language == 'English':
                _label = LabelEng.query.filter_by(text=name).first()

            if language == 'Polish':
                _label = LabelPol.query.filter_by(text=name).first()

            _segmentation.label_id = _label.label_id

            db.session.commit()

            return redirect('/image?image_id=' + _segmentation.image_id)

        else:
            return render_template("label_assign.html", form=form)

    else:
        error = "You need an existing segmentation to assign a label."
        return render_template("label_error.html", error=error)


@label.route('/label_search')
def label_search():
    if 'text' in request.args:
        _text = request.args.get('text')
        _eng = LabelEng.query.filter(LabelEng.text.ilike(_text)).all()
        _pol = LabelPol.query.filter(LabelPol.text.ilike(_text)).all()

        if _eng or _pol:
            return render_template("label_search.html", eng=_eng, pol=_pol, error=None)
        else:
            error = "Unable to find " + _text
            return render_template("label_search.html", eng=None, pol=None, error=error)
    else:
        error = "Unable to search for nothing."
        return render_template("label_error.html", error=error)


@label.route('/label_list')
def label_list():
    if 'page' in request.args:
        _page = request.args.get('page', type=int)
        if _page < 1:
            _page = 1
    else:
        _page = 1
    if 'lang' in request.args:
        _lang = request.args.get('lang', type=str)
    else:
        _lang = 'en'

    if _lang == 'pl':
        _labels = LabelPol.query.paginate(page=_page, per_page=50, error_out=False)
    else:
        _labels = LabelEng.query.paginate(page=_page, per_page=50, error_out=False)

    if _labels.has_next:
        next_url = url_for('label.label_list', page=_labels.next_num)
    else:
        next_url = None
    if _labels.has_prev:
        prev_url = url_for('label.label_list', page=_labels.prev_num)
    else:
        prev_url = None

    return render_template('label_list.html', labels=_labels, next_url=next_url, prev_url=prev_url, lang=_lang)


@label.route('/label_tree')
def label_tree():
    if 'label_id' in request.args:
        _label_id = request.args.get('label_id')
        _label = Label.query \
            .options(db.joinedload(Label.id == LabelEng.label_id)) \
            .filter_by(id=_label_id) \
            .first()
        _children = db.session.query(Label, LabelEng).filter_by(id=_label_id) \
            .join(LabelEng) \
            .first()

        result = db.engine.execute(
            "SELECT label.id, label_eng.text FROM label JOIN label_eng ON label.id = label_eng.label_id WHERE label.id ='" + _label_id + "'")

        result2 = db.engine.execute(
            "SELECT label.id, label_eng.text FROM label JOIN label_eng ON label.id = label_eng.label_id WHERE label.parent_id ='" + _label_id + "'"
        )
    else:
        return '500 BAD PATH'

    print(_label)

    return render_template("label_tree.html", label=_label, children=_children, result=result, result2=result2)
