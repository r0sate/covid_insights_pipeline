from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from .agent_bridge import get_response
from .utils.serialize import serialize

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", ping_interval=25, ping_timeout=600)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("user_message")
def handle_message(data):
    msg = data.get("message", "")
    response = get_response(msg)


    if response.get("error"):
        # Envia erro estruturado
        emit("agent_response", {"error": True,
            "code": response.get("code", 500)
        })
    else:
        # Envia resposta normal
        safe_response = serialize(response.get("response", ""))
        emit("agent_response", {"response": safe_response})

def run_app():
    socketio.run(app, debug=True)
