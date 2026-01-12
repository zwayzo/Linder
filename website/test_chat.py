import socketio
import time

USER_ID =2
OTHER_ID = 1

sio = socketio.Client()

@sio.event
def connect():
    print("Connected")
    sio.emit("join_chat", {
        "user_id": USER_ID,
        "other_user_id": OTHER_ID
    })

@sio.on("joined")
def joined(data):
    print("Joined room:", data["room"])

@sio.on("receive_private_message")
def receive(msg):
    print("📩", msg)

sio.connect("http://127.0.0.1:5000")

# send messages manually from code
while True:
    text = input("You: ")
    sio.emit("send_private_message", {
        "sender_id": USER_ID,
        "receiver_id": OTHER_ID,
        "content": text
    })
