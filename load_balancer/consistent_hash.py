import mmh3


class ConsistentHash:
    def __init__(self, num_slots=160, num_replicas=3):
        self.num_slots = num_slots
        self.num_replicas = num_replicas
        self.hash_ring = {}
        self.server_names = []
        self.server_requests = {}

    def _hash(self, key):
        """Generic hash function using MD3."""
        return mmh3.hash(key) % self.num_slots
    
    

    def add_server(self, server_name):
        if server_name in self.server_names:
            return  # Server already exists

        self.server_names.append(server_name)
        for i in range(self.num_replicas):
            virtual_node = f"{server_name}#{i}"
            self.hash_ring[self._hash(virtual_node)] = server_name
        self.server_requests[server_name] = 0
        print(f"Added server: {server_name}")

    def remove_server(self, server_name):
        if server_name not in self.server_names:
            return  # Server not found

        self.server_names.remove(server_name)
        for i in range(self.num_replicas):
            virtual_node = f"{server_name}#{i}"
            del self.hash_ring[self._hash(virtual_node)]
        del self.server_requests[server_name]
        print(f"Removed server: {server_name}")

    def get_server(self, request_id):
        if not self.hash_ring:
            return None
        hash_value = self._hash(request_id)
        keys = sorted(self.hash_ring.keys())
        for key in keys:
            if key >= hash_value:
                server = self.hash_ring[key]
                self.server_requests[server] += 1
                print(f"Request {request_id} assigned to server {server}")
                return server
        server = self.hash_ring[keys[0]]  # Wrap around if necessary
        self.server_requests[server] += 1
        print(f"Request {request_id} assigned to server {server}")
        return server
