from flask import request, Blueprint, redirect, url_for, flash

from ..database import Image, ImageGroup, db

group = Blueprint('group', __name__)


@group.route("/group_create")
def add_group():
    if 'this' in request.args and 'that' in request.args:
        _this = request.args.get('this')
        _that = request.args.get('that')

        _this_entry = Image.query.filter(Image.id == _this).first()
        _that_entry = Image.query.filter(Image.id == _that).first()

        _this_group = _this_entry.group_id
        _that_group = _that_entry.group_id

        if _this_group is not None:
            _group_id = _this_group
        else:
            if _that_group is not None:
                _group_id = _that_group
            else:
                _group_id = None

        if _group_id is not None:
            _this_entry.group_id = _group_id
            _that_entry.group_id = _group_id
            db.session.commit()
        else:
            _group = ImageGroup()
            db.session.add(_group)
            db.session.commit()
            _this_entry.group_id = _group.id
            _that_entry.group_id = _group.id
            db.session.commit()
    flash("Group added.")
    return redirect(request.referrer or url_for("home.index"))
