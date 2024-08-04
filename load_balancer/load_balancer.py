import os
import docker
from flask import Flask, request, redirect, jsonify
import socket
from consistent_hash import ConsistentHash
import logging
import json
import requests
from pythonjsonlogger import jsonlogger
import time
import threading

app = Flask(__name__)

# Initialize hash ring with no servers initially
hash_ring = ConsistentHash(num_replicas=3)

client = docker.from_env()

server_counter = 1

# Logging Setup
log_directory = '/app/logs'
os.makedirs(log_directory, exist_ok=True)  # Create if doesn't exist
log_file = os.path.join(log_directory, 'requests.log')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logHandler = logging.FileHandler(log_file)
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')  # Exact format
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# Server Creation Logic (within `update_server_list` function)
def create_server_instance():
    global server_counter
    try:
        image = client.images.get("server")  # Get the server image
        container_name = f"server-{server_counter}"
        container = client.containers.run(
            image,
            name=container_name,  # Unique name
            detach=True,
            ports={"5000/tcp": None}, 
            environment={"SERVER_ID": container_name},
            network="load_balancer_network",
            remove=True # Remove container after it stops
        )
        logger.info(f"Created new server instance: {container.name}")
        server_counter += 1
    except docker.errors.ImageNotFound:
        logger.error("Docker image 'server' not found.")
    except docker.errors.APIError as e:
        logger.error(f"Error creating server instance: {e}")

def create_initial_servers(num_servers=3):
    """Create an initial set of server instances when the load balancer starts."""
    for _ in range(num_servers):
        create_server_instance()

# Server Discovery (Updated)
def update_server_list():
    while True:
        containers = client.containers.list(filters={"name": "server"})

        # Create new instances if needed (adjust the logic based on your criteria)
        if len(containers) < 3:  # Example: Maintain at least 3 servers
            create_server_instance()
        
        # Update hash ring
        for container in containers:
            hash_ring.add_server(container.name)
        time.sleep(60)  # Update every 60 seconds


# Create and start a separate thread for server discovery
discovery_thread = threading.Thread(target=update_server_list)
discovery_thread.daemon = True  # Allow the thread to exit when the main program ends
discovery_thread.start()


@app.route("/", methods=["GET"])
def landing_page():
    return "Load Balancer is active."


@app.route("/stats", methods=["GET"])
def get_stats():
    return jsonify(hash_ring.server_requests), 200


@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def load_balancer(path):
    try:
        server = hash_ring.get_server(request.remote_addr)

        if server:
            # Fetch and include message from the server
            response = requests.get(f"http://{server}:5000/{path}", timeout=5)
            response_data = response.json()
            server_message = response_data.get("message", "Server message not available")

            # Construct log_message 
            log_message = {
                "remote_addr": request.remote_addr,
                "server": server,
                "method": request.method,
                "message": server_message
            }

            # Log the request details in JSON
            logger.info(json.dumps(log_message))  # Log after successful request

            return response.content, response.status_code
        else:
            logger.error("No available server", extra={"remote_addr": request.remote_addr, "method": request.method, "path": path})
            return "No available server", 503

    except (docker.errors.APIError, socket.error, requests.exceptions.RequestException, KeyError) as e:
        # Log errors with details and context
        logger.error(str(e), exc_info=True, extra=log_message)  
        if isinstance(e, docker.errors.APIError):
            return "Internal Server Error", 500
        elif isinstance(e, socket.error):
            return "Bad Gateway", 502
        else:
            return "Service Unavailable", 503


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    logger.info("Healthcheck successful")
    return "OK", 200

if __name__ == "__main__":
    create_initial_servers()  # Create servers before starting Flask app
    discovery_thread = threading.Thread(target=update_server_list)
    discovery_thread.daemon = True
    discovery_thread.start()
    app.run(host="0.0.0.0", port=80)
