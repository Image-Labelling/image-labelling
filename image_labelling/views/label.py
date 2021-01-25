from flask import request, Blueprint, render_template, redirect, flash

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


@label.route('/label_search')
def label_search():
    if 'text' in request.args:
        return "Here's label " + request.args.get('text')
    else:
        return "I can't search for nothing"


@label.route('/label_list')
def label_list():
    return "Here's some labels"
