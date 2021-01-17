from flask import Flask, render_template, request, Blueprint, render_template, flash, redirect
from flask import current_app
from flask_login import LoginManager, login_required
from image_labelling.database import Label
from image_labelling.form import LabelForm

group = Blueprint('group', __name__)

@group.route("/group", methods=['GET', 'POST'])
def add_label():
    form = LabelForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            parent, name, language = form.data['parent'], form.data['name'], form.data['language']
            new_label = Label()
            form.populate_obj(new_label)
            return redirect('/label')

    return render_template('label.html', form=form)
