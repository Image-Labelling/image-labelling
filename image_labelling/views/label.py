from flask import Flask, render_template, request, Blueprint, render_template, flash, redirect
from flask import current_app
from flask_login import LoginManager, login_required
from image_labelling.database import Label
from image_labelling.form import LabelForm

label = Blueprint('label', __name__)


@label.route("/label", methods=['GET', 'POST'])
def add_label():
    form = LabelForm()
    if request.method == 'POST' and form.validate():
        parent, name, language = form.data.parent, form.data.name, form.data.language
        new_label = Label()
        form.populate_obj(new_label)
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
