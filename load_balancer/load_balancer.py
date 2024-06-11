import os
import docker
from flask import Flask, request, redirect, jsonify
import socket
from consistent_hash import ConsistentHash
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
hash_ring = ConsistentHash(num_replicas=3)

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

@app.route('/', methods=['GET'])
def landing_page():
    return "Load Balancer is active."

@app.route('/stats', methods=['GET'])
def get_stats():
    return jsonify(hash_ring.server_requests), 200

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE']) # allow all methods
def load_balancer(path):
    try:
        containers = client.containers.list(filters={"name": "server"})  # Use service name
        for container in containers:
            hash_ring.add_server(container.name)

        server = hash_ring.get_server(request.remote_addr)
        if server:
            return redirect(f'http://{server}:5000/{path}', code=307)
        else:
            return "No available server", 503  # Service Unavailable
    except docker.errors.APIError as e:
        app.logger.error(f"Docker API error: {e}")
        return "Internal Server Error", 500
    except socket.error as e:
        app.logger.error(f"Socket error: {e}")
        return "Bad Gateway", 502
    except KeyError as e:  # In case server not found in hash_ring
        app.logger.error(f"Server not found: {e}")
        return "Service Unavailable", 503
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    """Used to check the health of the load balancer."""
    return "OK", 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
