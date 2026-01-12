from flask import Blueprint
from flask_socketio import join_room, emit
from . import socketio, db
from .models import Message

chat = Blueprint("chat", __name__)

def get_room(user1, user2):
    return f"chat_{min(user1, user2)}_{max(user1, user2)}"

@socketio.on("join_chat")
def join_chat(data):
    user_id = data["user_id"]
    other_user_id = data["other_user_id"]

    room = get_room(user_id, other_user_id)
    join_room(room)

    emit("joined", {"room": room})

@socketio.on("send_private_message")
def send_private_message(data):
    sender = data["sender_id"]
    receiver = data["receiver_id"]
    content = data["content"]

    room = get_room(sender, receiver)

    msg = Message(
        room=room,
        sender_id=sender,
        receiver_id=receiver,
        content=content
    )

    db.session.add(msg)
    db.session.commit()

    emit("receive_private_message", {
        "sender_id": sender,
        "content": content
    }, room=room)
