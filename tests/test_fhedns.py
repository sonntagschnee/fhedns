import fhedns
import unittest
import numpy as np
import logging
import time


# Update hosts
names = np.random.randint(0, 2, (16, fhedns.Store.QUERY_LENGTH), dtype=np.uint8)
ips = np.random.randint(0, 2, (16, 32), dtype=np.uint8)

class TestStore(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    def setUp(self):
        self.dns = fhedns.Store()

        # Update hosts
        self.dns.update(names, ips)

    def tearDown(self):
        self.dns.circuit.cleanup()

    def test_update_is_compiled(self):
        self.assertIsNotNone(self.dns.circuit)

    def test_lookup_benchmark(self):
        # Generate keys
        self.dns.generate_keys(1)

        query = np.repeat(0, self.dns.QUERY_LENGTH)
        encrypted_query = self.dns.circuit.encrypt(query)

        start = time.time()
        
        # Lookup query
        self.dns.lookup(encrypted_query)
        
        end = time.time()
        
        self.logger.info('Ran lookup() %.2f in seconds.' % (end - start))

    def test_generate_keys_benchmark(self):
        start = time.time()
        
        # Generate keys
        self.dns.generate_keys(1)
        
        end = time.time()
        
        self.logger.info('Ran generate_keys() %.2f in seconds.' % (end - start))
