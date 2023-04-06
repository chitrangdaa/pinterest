from flask import render_template, url_for, flash, redirect, request, Blueprint
from pinterest.pin.forms import PinCreation, PinboardCreation, AddPinToPinboard, FilteredPins,CommentForm
from flask_login import login_required, current_user
from pinterest import db
from pinterest.models import Pins, Category, User, Pinboard, SavePin, Board_of_Pins, Vote, Comments
#import cloudinary.uploader

from pinterest.pin.utils import save_picture

pin = Blueprint('pin', __name__)


@pin.route("/pin/create", methods=['GET', 'POST'])
@login_required
def create_new():
    """Creating new pin"""
    category_data = Category.query.all()
    form = PinCreation()
    if form.validate_on_submit():
        picture_file = save_picture(form.picture.data)
        #upload_result = cloudinary.uploader.upload(form.picture.data, folder="Pins")
        #print(f'------upload result---{upload_result}')

        pin = Pins(
            title=form.title.data,
            pin_content=form.pin_content.data,
            is_private=form.is_private.data,
            author=current_user,
            category_id=request.form.get("category"),
            image_file=picture_file
        )
        db.session.add(pin)
        db.session.commit()
        flash("New Pin is created", category='success')
        return redirect(url_for("pin.view_pins"))
    return render_template('create_pin.html', form=form, category_data=category_data, legend="Create New Pin")


@pin.route("/home")
@pin.route("/pin/views", methods=['GET'])
@login_required
def view_pins():
    """Showing all the pins"""
    page = request.args.get('page', 1, type=int)
    pins = Pins.query.filter_by(is_private=False).paginate(page=page, per_page=10)
    return render_template('view_pins.html', pins=pins)


@pin.route("/createdpin", methods=['GET'])
@login_required
def view_created_pins():
    """ user's created pins"""
    user = User.query.get(current_user.id)
    pins = user.pins
    return render_template('createdpins.html', pins=pins)


@pin.route("/createdpin/delete/<pin_id>", methods=['GET'])
@login_required
def delete_pins(pin_id):
    """Delete a pin"""
    pin = Pins.query.get_or_404(pin_id)
    db.session.delete(pin)
    db.session.commit()
    flash(' Your Pin has been deleted', category='success')
    return redirect(url_for('pin.view_created_pins'))


@pin.route("/createdpin/update/<pin_id>", methods=['GET', 'POST'])
@login_required
def update_pins(pin_id):
    """Update pin"""
    pin = Pins.query.get_or_404(pin_id)
    form = PinCreation()
    if form.validate_on_submit():
        pin.title = form.title.data
        pin.pin_content = form.pin_content.data
        pin.is_private = form.is_private.data
        db.session.commit()
        flash('Your Pin has been updated', 'success')
        return redirect(url_for('pin.view_created_pins'))
    elif request.method == 'GET':
        form.title.data = pin.title  # for filling values
        form.pin_content.data = pin.pin_content
        form.is_private.data = pin.is_private

    return render_template('update_pin.html', legend='Update Pin', form=form)


@pin.route("/board/create", methods=['GET', 'POST'])
@login_required
def create_pin_board():
    """Creating a  new pin board"""
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


@pin.route("/pin/save/<pin_id>", methods=['GET', 'POST'])
@login_required
def save_pin(pin_id):
    """For saving pins"""
    save = SavePin.query.filter_by(user_id=current_user.id, pin_id=pin_id).all()
    if not save:
        savepin = SavePin(
            user_id=current_user.id,
            pin_id=pin_id
        )
        db.session.add(savepin)
        db.session.commit()

    flash('Pin is saved', category='success')
    return redirect(url_for('pin.view_pins'))


@pin.route("/pin/unsave/<pin_id>", methods=['GET', 'POST'])
@login_required
def unsave_pin(pin_id):
    """ To remove pin from saved collection"""
    pin = SavePin.query.filter_by(pin_id=pin_id).all()
    for p in pin:
        db.session.delete(p)
    db.session.commit()
    flash('Pin removed from saved collection', category='success')
    return redirect(url_for('pin.view_pins'))


@pin.route("/savedpins", methods=['GET'])
@login_required
def view_saved_pins():
    """For viewing all the saved pins"""
    pins = db.session.query(Pins).join(SavePin).filter(SavePin.user_id == current_user.id)
    return render_template('savedpins.html', pins=pins)


@pin.route("/pin/<int:pin_id>", methods=['GET', 'POST'])
@login_required
def view_detailed_pin(pin_id):
    """ To view detailed pin"""
    alreadyliked = Vote.query.filter_by(user_id=current_user.id, pin_id=pin_id).all()
    if alreadyliked:
        likee = True
    else:
        likee = False
    form = AddPinToPinboard()
    commentform = CommentForm()
    pin = Pins.query.get_or_404(pin_id)
    boards = Pinboard.query.filter_by(user_id=current_user.id)
    if commentform.validate_on_submit():
        comment = Comments(
            user_id=current_user.id,
            pin_id=pin_id,
            comment=commentform.comment.data
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment is posted', category='success')
        return redirect(url_for('pin.view_detailed_pin', pin_id=pin_id))
    if form.validate_on_submit():
        flash("Pin added to your pinboard", category='success')
        board_id = request.form.get("category")
        return redirect(url_for('pin.add_to_pinboard', pin_id=pin_id, board_id=board_id))
    return render_template('pin.html', pin=pin, boards=boards, form=form, like=likee, commentform=commentform)


@pin.route("/pin/<int:pin_id>/<int:board_id>", methods=['GET', 'POST'])
@login_required
def add_to_pinboard(pin_id, board_id):
    """ To add a pin to already created pin-boards"""
    board_of_pins = Board_of_Pins(
        pin_id=pin_id,
        pinboard_id=board_id
    )
    db.session.add(board_of_pins)
    db.session.commit()
    return redirect(url_for('pin.view_detailed_pin', pin_id=pin_id))


@pin.route("/pinboard/view", methods=['GET', 'POST'])
@login_required
def view_pinboard():
    """To view pin-board"""
    pinboard = Pinboard.query.filter_by(user_id=current_user.id).all()
    return render_template('pinboard.html', pinboard=pinboard)


@pin.route("/pinboard/<board_id>", methods=['GET', 'POST'])
@login_required
def view_pins_in_board(board_id):
    """To view pins in board"""
    pins = db.session.query(Pins).join(Board_of_Pins).filter(Board_of_Pins.pinboard_id == board_id)
    return render_template('view_pins_in_pinboard.html', pins=pins, board_id=board_id)


@pin.route("/board/update/<board_id>", methods=['GET', 'POST'])
@login_required
def update_pinboard(board_id):
    """Update Pinboard"""
    pinboard = Pinboard.query.filter_by(id=board_id).first()
    form = PinboardCreation()
    if form.validate_on_submit():
        pinboard.pin_board_name = form.pin_board_name.data
        pinboard.board_is_private = form.board_is_private.data
        db.session.commit()
        flash('pinboard is updated', category='success')
        return redirect(url_for('pin.view_pinboard'))
    elif request.method == 'GET':
        form.pin_board_name.data = pinboard.pin_board_name
        form.board_is_private.data = pinboard.board_is_private
    return render_template('create_board.html', form=form)


@pin.route("/pin/remove/<board_id>/<pin_id>", methods=['GET', 'POST'])
@login_required
def remove_pin_from_board(board_id, pin_id):
    """Removing a pin from a board"""
    pin_in_board = Board_of_Pins.query.filter_by(pinboard_id=board_id, pin_id=pin_id).first()
    db.session.delete(pin_in_board)
    db.session.commit()
    flash('Pin has been removed from this pinboard', category='success')
    return redirect(url_for('pin.view_pins_in_board', board_id=board_id))


@pin.route("/pinboard/delete/<int:board_id>")
@login_required
def delete_pinboard(board_id):
    """For deleting entire board"""
    board = Pinboard.query.get_or_404(board_id)
    pin_in_board = Board_of_Pins.query.filter_by(pinboard_id=board_id).all()
    for board in pin_in_board:
        db.session.delete(board)
    db.session.delete(board)
    db.session.commit()
    flash('Pinboard is deleted', category='success')
    return redirect(url_for('pin.view_pinboard'))


@pin.route("/pins/filter", methods=['GET', 'POST'])
@login_required
def filter_pins_by_category():
    """Filter pins according to categories"""
    category_data = Category.query.all()
    form = FilteredPins()
    if form.validate_on_submit():
        return redirect(url_for('pin.view_filtered_pins', category_id=request.form.get("category")))
    return render_template('filter_pins.html', category_data=category_data, form=form)


@pin.route("/pins/filter/view/<category_id>")
@login_required
def view_filtered_pins(category_id):
    """Viewing pins according to various categories"""
    page = request.args.get('page', 1, type=int)
    pins = Pins.query.filter_by(category_id=category_id, is_private=False).paginate(page=page, per_page=10)
    return render_template('view_pins.html', pins=pins)


@pin.route("/pin/like/<pin_id>")
@login_required
def like(pin_id):
    """To Like a Pin"""
    alreadyliked = Vote.query.filter_by(user_id=current_user.id, pin_id=pin_id).all()
    if not alreadyliked:
        like = Vote(
            user_id=current_user.id,
            pin_id=pin_id
        )
        db.session.add(like)
        db.session.commit()

    return redirect(url_for('pin.view_detailed_pin', pin_id=pin_id))


@pin.route("/pin/unlike/<pin_id>")
@login_required
def unlike(pin_id):
    """ To Unlike a pin"""
    unlike = Vote.query.filter_by(user_id=current_user.id, pin_id=pin_id).first()
    db.session.delete(unlike)
    db.session.commit()
    return redirect(url_for('pin.view_detailed_pin', pin_id=pin_id))


@pin.route("/pin/comment/<pin_id>", methods=['GET', 'POST'])
@login_required
def comment(pin_id):
    """To add comment on a Pin"""
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comments(
            user_id=current_user.id,
            pin_id=pin_id,
            comment=form.comment.data
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment is posted', category='success')
    return render_template('comment.html', form=form)


@pin.route("/pin/displaycomment/<pin_id>", methods=['GET', 'POST'])
@login_required
def display_comments(pin_id):
    """Displaying comments"""
    pin_comments = Comments.query.filter_by(pin_id=pin_id)
    return render_template('pin.html', pin_comments=pin_comments)


@pin.route("/profile/<pin_id>", methods=['GET'])
@login_required
def profile(pin_id):
    """For viewing other user's profile"""
    pin = Pins.query.filter_by(id=pin_id).first()
    user = User.query.filter_by(id=pin.author.id).first()
    return render_template('profile.html', pin=pin, user=user)


@pin.route("/profile/pin-board/<user>", methods=['GET'])
@login_required
def display_profile_pinboard(user):
    """To view pin-boards of other users """
    user = User.query.filter_by(id=user).first()
    pinboard = user.pinboard.filter_by(board_is_private=False).all()
    return render_template('pinboard.html', pinboard=pinboard)


@pin.route("/profile/pins/<user>", methods=['GET'])
@login_required
def profile_created_pins(user):
    """To view pins created by other users"""
    user = User.query.filter_by(id=user).first()
    page = request.args.get('page', 1, type=int)
    pins = user.pins.filter_by(is_private=False).paginate(page=page, per_page=10)
    return render_template('view_pins.html', pins=pins)
