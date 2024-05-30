from flask import Flask, request, redirect
from consistent_hash import ConsistentHash

app = Flask(__name__)
hash_ring = ConsistentHash()

# Add servers to the hash ring
hash_ring.add_server('sub-server-1')
hash_ring.add_server('sub-server-2')
hash_ring.add_server('sub-server-3')
hash_ring.add_server('sub-server-4')

@app.route('/', defaults={'path': ''})  # Catch-all route
@app.route('/<path:path>')
def load_balancer(path):
    server = hash_ring.get_server(request.remote_addr)  # Get the server based on the request's IP
    return redirect(f'http://{server}:5000/{path}', code=307)  # Redirect with original request method and body

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  # Expose the balancer on port 80
