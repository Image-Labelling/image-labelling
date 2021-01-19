from flask import Blueprint, redirect, render_template, request, flash

image = Blueprint('image', __name__)


@image.route('/image')
def show_image():
    if 'image_id' in request.args:
        _image_id = request.args.get('image_id')
        return "Fancy page that shows you stuff based on image_id."

    else:
        return "Ya need an image id, dingus."