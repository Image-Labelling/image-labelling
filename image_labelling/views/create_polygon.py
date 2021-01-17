from flask import Blueprint, render_template, request

create_polygon = Blueprint('create_polygon', __name__)


@create_polygon.route("/createpolygon")
def createpolygon():
    image_id=request.args.get('image_id', type=str)
    return render_template("createPolygon.html", image_id=image_id)
