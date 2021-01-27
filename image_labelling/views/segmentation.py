from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from ..database import Point

segmentation = Blueprint('segmentation', __name__)


@segmentation.route('/segmentation')
@cross_origin()
def get_segmentation():
    if 'segmentation_id' in request.args:
        _segmentation_id = request.args.get('segmentation_id')
        _points = Point.query.filter(Point.segmentation_id == _segmentation_id).all()
        json = {'data': []}
        for point in _points:
            json['data'].append(point.serialized)

        return jsonify(json)

    else:
        pass
