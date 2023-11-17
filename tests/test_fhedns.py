import fhedns
import unittest
import numpy as np
import logging
import time


# Numpy random seed
np.random.seed(3)

# Update hosts
index = 3
names = np.random.randint(0, 2, (16, fhedns.Store.QUERY_LENGTH), dtype=np.uint8)
names[index,:] = 1
ips = np.random.randint(0, 2, (16, 32), dtype=np.uint8)

class TestStore(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    def setUp(self):
        self.dns = fhedns.Store()

        # Update hosts
        self.dns.update(names, ips)

        # Generate keys
        self.dns.generate_keys(1)

    def tearDown(self):
        self.dns.circuit.cleanup()

    def test_update_is_compiled(self):
        self.assertIsNotNone(self.dns.circuit)

    def test_query(self):
        #query = np.repeat(0, self.dns.QUERY_LENGTH)
        query = names[index]
        encrypted_query = self.dns.circuit.encrypt(query)

        # Lookup query
        encrypted_result = self.dns.lookup(encrypted_query)

        # Decrypt
        result = self.dns.circuit.decrypt(encrypted_result)

        self.assertTrue(np.array_equal(result, ips[index]))

    def test_lookup_benchmark(self):
        query = np.repeat(0, self.dns.QUERY_LENGTH)
        encrypted_query = self.dns.circuit.encrypt(query)

        start = time.time()
        
        # Lookup query
        self.dns.lookup(encrypted_query)
        
        end = time.time()
        
        self.logger.info('Ran lookup() %.2f in seconds.' % (end - start))
