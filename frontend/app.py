from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from .agent_bridge import get_response

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("user_message")
def handle_message(data):
    msg = data.get("message", "")
    response = get_response(msg)
    emit("agent_response", {"response": response})

def run_app():
    socketio.run(app, debug=True)
