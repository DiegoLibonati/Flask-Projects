from foro import create_app
from flask_socketio import SocketIO,send
from flask_login import login_required, current_user

app = create_app()
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('message')
@login_required
def handleMessage(msg):
    send(f'<img src="/static/profilephotos/{current_user.profile_photo}" alt="{current_user.username}"><h2>{current_user.username}</h2>:{msg}', broadcast=True)

if __name__ == "__main__":
    socketio.run(app,debug=True)