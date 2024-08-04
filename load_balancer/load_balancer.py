import os
import docker
from flask import Flask, request, redirect, jsonify
import socket
from consistent_hash import ConsistentHash
import logging
import json
import requests
from pythonjsonlogger import jsonlogger

app = Flask(__name__)

hash_ring = ConsistentHash(num_replicas=3)

# Ensure the log directory exists
log_directory = '/app/logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# JSON Logging Setup
log_file = os.path.join(log_directory, 'requests.log')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logHandler = logging.FileHandler(log_file)
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

client = docker.DockerClient(base_url="unix://var/run/docker.sock")

@app.route("/", methods=["GET"])
def landing_page():
    return "Load Balancer is active."

@app.route("/stats", methods=["GET"])
def get_stats():
    return jsonify(hash_ring.server_requests), 200

@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def load_balancer(path):
    try:
        containers = client.containers.list(filters={"name": "server"})
        current_servers = set(container.name for container in containers)
        existing_servers = set(hash_ring.server_names)
        
        # Add new servers
        for server in current_servers - existing_servers:
            hash_ring.add_server(server)
        
        # Remove old servers
        for server in existing_servers - current_servers:
            hash_ring.remove_server(server)

        server = hash_ring.get_server(request.remote_addr)
        
        # Check if a server was found
        if server:
            # Fetch message from the server
            try:
                response = requests.get(f"http://{server}:5000/")
                response_data = response.json()
                server_message = response_data.get("message", "Server message not available")
            except requests.exceptions.RequestException as e:
                # If fetching the message fails, still log but with an error message
                server_message = f"Error fetching message from server: {e}"

            # Construct log_message
            log_message = {
                "remote_addr": request.remote_addr,
                "server": server,
                "method": request.method,
                "message": server_message
            }
            
            # Log the request details in JSON
            logger.info(json.dumps(log_message))

            return redirect(f"http://{server}:5000/{path}", code=307)
    
        else:
            logger.error("No available server", extra={"remote_addr": request.remote_addr, "method": request.method, "path": path})
            return "No available server", 503

    except (docker.errors.APIError, socket.error, KeyError) as e:
        # Log errors with details and context
        logger.error(str(e), exc_info=True, extra=log_message) 
        if isinstance(e, docker.errors.APIError):
            return "Internal Server Error", 500
        elif isinstance(e, socket.error):
            return "Bad Gateway", 502
        else:  # KeyError (Server not found)
            return "Service Unavailable", 503

@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    logger.info("Healthcheck successful")
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
