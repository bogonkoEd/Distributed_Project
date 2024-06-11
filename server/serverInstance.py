import os
from flask import Flask, jsonify, send_from_directory  
import socket

app = Flask(__name__)

# Get server ID from environment variable set in Dockerfile
server_id = os.environ.get('SERVER_ID', 'Default')

@app.route('/')
def home():
    response = {
        "message": f"Hello from Server: {server_id} at {socket.gethostbyname(socket.gethostname())}", 
        "status": "successful"
    }
    return jsonify(response), 200


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '', 200  # Empty response with 200 OK status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)