from flask import render_template, url_for, flash, redirect, request, Blueprint
from pinterest.pin.forms import PinCreation, PinboardCreation
from flask_login import login_required, current_user
from pinterest import db
from pinterest.models import Pins, Category, User, Pinboard
from pinterest.pin.utils import save_picture

pin = Blueprint('pin', __name__)


@login_required
@pin.route("/pin/create", methods=['GET', 'POST'])
def create_new():
    """Creating new pin"""
    category_data = Category.query.all()
    form = PinCreation()
    if form.validate_on_submit():
        picture_file = save_picture(form.picture.data)
        # saving image file name in database
        print(f'request.form {request.form.get("category")}')

        pin = Pins(
            title=form.title.data,
            pin_content=form.pin_content.data,
            is_private=form.is_private.data,
            is_notification_active=form.is_notification_active.data,
            author=current_user,
            category_id=request.form.get("category"),
            image_file=picture_file

        )
        db.session.add(pin)
        db.session.commit()
        flash("New Pin is created", category='success')
        return redirect(url_for("main.home"))
    return render_template('create_pin.html', form=form, category_data=category_data, legend="Create New Pin")


@login_required
@pin.route("/pin/view", methods=['GET'])
def view_pins():
    """Showing all the pins"""
    # db.pins.filter_by(is_private=False)
    pins = Pins.query.filter_by(is_private=False)
    return render_template('view_pins.html', pins=pins)


@login_required
@pin.route("/createdpin", methods=['GET'])
def view_created_pins():
    """ user's created pins"""
    user = User.query.get(current_user.id)
    pins = user.pins
    return render_template('createdpins.html', pins=pins)


@login_required
@pin.route("/createdpin/delete/<pin_id>", methods=['GET'])
def delete_pins(pin_id):
    """Delete a pin"""
    pin = Pins.query.get_or_404(pin_id)
    db.session.delete(pin)
    db.session.commit()
    flash(' Your Pin has been deleted', category='success')
    return redirect(url_for('pin.view_created_pins'))


@login_required
@pin.route("/createdpin/update/<pin_id>", methods=['GET', 'POST'])
def update_pins(pin_id):
    """Update pin"""
    pin = Pins.query.get_or_404(pin_id)
    form = PinCreation()
    if form.validate_on_submit():
        pin.title = form.title.data
        pin.pin_content = form.pin_content.data

        db.session.commit()
        flash('Your Pin has been updated', 'success')
        return redirect(url_for('pin.view_created_pins'))
    elif request.method == 'GET':
        form.title.data = pin.title  # for filling values
        form.pin_content.data = pin.pin_content

    return render_template('update_pin.html', legend='Update Pin', form=form)


@login_required
@pin.route("/board/create", methods=['GET', 'POST'])
def create_pin_board():
    """Creating a pin board"""
    form = PinboardCreation()
    if form.validate_on_submit():
        pinboard = Pinboard(
            pin_board_name=form.pin_board_name.data,
            board_is_private=form.board_is_private.data,
            user_id=current_user.id
        )
        db.session.add(pinboard)
        db.session.commit()
        flash('Your Pinboard is created', 'success')
    return render_template('create_board.html', form=form)

# @login_required
# @pin.route("/pin/save", methods=['GET','POST'])
# def save_pins():
