import hashlib


class ConsistentHash:
    def _init_(self, num_replicas=3, num_slots=512):
        self.num_replicas = num_replicas
        self.num_slots = num_slots
        self.hash_ring = {}  # {hash: server_name}
        self.servers = set()

    def _hash(self, key):
        """Hash a key to a slot on the ring."""
        return int(hashlib.md5(key.encode()).hexdigest(), 16) % self.num_slots

    def add_server(self, server_name):
        """Add a server to the hash ring."""
        self.servers.add(server_name)
        for i in range(self.num_replicas):
            virtual_node = f"{server_name}:{i}"
            hash_value = self._hash(virtual_node)
            self.hash_ring[hash_value] = server_name

   