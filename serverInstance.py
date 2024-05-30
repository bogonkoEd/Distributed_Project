from flask import Flask, jsonify

app = Flask(__name__)

# Get server ID from environment variable set in Dockerfile
server_id = os.environ.get('SERVER_ID', 'Default')

@app.route('/home', methods=['GET'])
def home():
    response = {
        "message": f"Hello from Server: {server_id}",
        "status": "successful"
    }
    return jsonify(response), 200

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '', 200  # Empty response with 200 OK status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
