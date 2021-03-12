# Local Imports
from messenger_app import create_messenger_app

# Flask Imports
from flask import session

# Flask Socket IO Imports
from flask_socketio import SocketIO, emit, join_room, leave_room

# Create Messenger App || Add Socket IO
app = create_messenger_app()
socketio = SocketIO(app)


##################################################################
# Socket Events
##################################################################
@socketio.on('enter', namespace='/thread')
def enter(message):
    """
    Event: Enters Chat Room
    """
    # Get Session Variables
    thread_id = session.get('thread_id')
    username = session.get('username')

    join_room(thread_id)

    # Emit Message
    emit('status', {'msg': f'{username} entered the chat room'}, room=thread_id)


@socketio.on('leave', namespace='/thread')
def leave(message):
    """
    Event: Leave Chat Room
    """
    # Get Session Variables
    thread_id = session.get('thread_id')
    username = session.get('username')

    leave_room(thread_id)

    # Emit Message
    emit('status', {'msg': f'{username} has left the room'}, room=thread_id)


@socketio.on('text', namespace='/thread')
def text(message):
    """
    Event: Send Message In Chat Room
    """
    # Get Session Variables
    thread_id = session.get('thread_id')
    username = session.get('username')

    # Emit Message
    emit('message', {'msg': f'{username}: ' + message['msg']}, room=thread_id)


if __name__ == '__main__':
    socketio.run(app)
