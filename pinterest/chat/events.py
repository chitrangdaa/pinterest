from flask import session
from flask_socketio import emit, join_room, leave_room
from ..models import User, Message
from pinterest import socketio, db


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = message.get('room', '')
    sender_id = message.get('sender_id')
    recipient_id = message.get('recipient_id')

    message_obj = Message.query.filter(Message.sender_id.in_([sender_id, recipient_id]),
                                       Message.recipient_id.in_([sender_id, recipient_id])).all()
    join_room(room)
    for msg in message_obj:
        sender = User.query.filter_by(id=msg.sender_id).first()
        emit('status', {'msg': f"{sender.username}: {msg.body}"}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    print("how you doing")
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    # room = session.get('room')

    msg = Message(
        body=message.get('msg'),
        recipient_id=message['recipient_id'],
        sender_id=message['sender_id']
    )

    db.session.add(msg)
    db.session.commit()
    room = message.get('room')

    socketio.emit('message', {'msg': f"{message['sender_id']}: {message['msg']}"}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)
