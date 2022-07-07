from flask import render_template
from flask_login import current_user
import secrets
import string
from . import chat
from .. import db
from ..models import User, Room


@chat.route('/chat/<recipient>', methods=['GET', 'POST'])
def chat_func(recipient):
    """Chat room"""
    user = User.query.filter_by(username=recipient).first_or_404()
    room = Room.query.filter(Room.sender_id.in_([current_user.id, user.id]),
                             Room.recipient_id.in_([current_user.id, user.id])).first()
    if not room:
        res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                      for i in range(10))
        room = Room(
            sender_id=current_user.id,
            recipient_id=user.id,
            room_name=res
        )
        db.session.add(room)
        db.session.commit()
    return render_template('chat.html', room=room.room_name, sender_id=current_user.id, recipient_id=user.id)

