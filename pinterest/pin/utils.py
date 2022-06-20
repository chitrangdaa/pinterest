import os
import secrets
from PIL import Image
from flask import current_app


def save_picture(form_picture):
    """For saving picture in our static directory"""
    random_hex = secrets.token_hex(8)  # to change name of image file uploaded
    _, f_ext = os.path.splitext(form_picture.filename)  # to extract our image's extension
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/pin_pics', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)  # saving picture in our project static/pin_pictures folder
    return picture_fn

