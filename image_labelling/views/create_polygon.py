import sys

from flask import Blueprint, render_template, request, redirect

from .. import db
from ..database import Point, Segmentation

create_polygon = Blueprint('create_polygon', __name__)


@create_polygon.route("/createpolygon", methods=['GET', 'POST'])
def createpolygon():
    _image_id = request.args.get('image_id', type=str)

    if request.method == 'POST':
        x_min = sys.maxsize
        y_min = sys.maxsize
        x_max = 0
        y_max = 0

        _segmentation = Segmentation()
        _segmentation.image_id = _image_id
        db.session.add(_segmentation)
        db.session.commit()
        i = 0
        for row in request.json:

            if row['x'] > x_max:
                x_max = row['x']

            if row['y'] > y_max:
                y_max = row['y']

            if row['x'] < x_min:
                x_min = row['x']

            if row['y'] < y_min:
                y_min = row['y']

            _point = Point()
            _point.order = i
            _point.segmentation_id = _segmentation.id
            _point.x_coord = int(row['x'])
            _point.y_coord = int(row['y'])
            i += 1
            db.session.add(_point)

        _segmentation.bounding_box_x = int(x_min)
        _segmentation.bounding_box_y = int(y_min)
        _segmentation.bounding_box_width = int(x_max - x_min)
        _segmentation.bounding_box_height = int(y_max - y_min)

        db.session.commit()
        return redirect('/image?image_id=' + _image_id)

    return render_template("createPolygon.html", image_id=_image_id)
