from concrete import fhe
import numpy as np
import math


class Store():
    QUERY_LENGTH = math.ceil(math.log2(37))*63
    circuit = None

    def __init__(self):
        pass

    def set_keys(self, keys: fhe.Keys):
        self.circuit.keys = keys

    def update(self, names: np.array, ips: np.array):
        self.names = names
        self.names_not = names_not = (np.logical_not(names)).astype(np.uint8)
        self.ips = ips

        @fhe.compiler({"query": "encrypted"})
        def lookup(query):
            # Test individual bits for quality using XNOR
            a = self.names
            a_not = self.names_not
            b = query
            index = a*b + (a_not*(1 - b))
        
            # Check if all bits were equal for each row
            index = np.sum(index, axis=1)
            index += 134
            index = fhe.bits(index)[9]
            index = index.reshape((-1, 1))

            # Filter IP
            ip = index*ips
            ip = np.sum(ip, axis=0)
        
            return ip

        inputset = [
                (np.repeat(0, self.QUERY_LENGTH).astype(np.uint8)),
                (np.repeat(1, self.QUERY_LENGTH).astype(np.uint8)),
                ]
        
        cfg = fhe.Configuration(auto_adjust_rounders=True, show_graph=True)
        self.circuit = lookup.compile(inputset, cfg)

    def generate_keys(self, seed=None):
        self.circuit.keys.generate(seed=seed)

    def lookup(self, encrypted_query):
        if self.circuit != None:
            return self.circuit.run(encrypted_query)
