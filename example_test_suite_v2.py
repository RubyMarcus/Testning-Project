import unittest
import pickle
import os
import platform
from compare_hashes import hash_file

class TestPickleStability(unittest.TestCase):

    def setUp(self):
        self.data = {
            "int": 123,
            "float": 123.456,
            "string": "test",
            "list": [1, 2, 3],
            "dict": {"key": "value"},
            "tuple": (1, 2, 3),
            "set": {1, 2, 3}
        }
        self.pickle_filename = "test_pickle.pkl"
        self.recursive_data = {}
        self.recursive_data["self"] = self.recursive_data

    def tearDown(self):
        if os.path.exists(self.pickle_filename):
            os.remove(self.pickle_filename)

    def test_pickle_stability(self):
        # Serialize the data
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(self.data, file)

        # Get the hash of the serialized file
        initial_hash = hash_file(self.pickle_filename)

        # Deserialize and serialize again
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(loaded_data, file)

        # Get the hash of the re-serialized file
        final_hash = hash_file(self.pickle_filename)

        # Check if both hashes are the same
        self.assertEqual(initial_hash, final_hash)

    def test_cross_environment_stability(self):
        # To be run manually on different operating systems and Python versions
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(self.data, file)

        hash_value = hash_file(self.pickle_filename)
        print(f"Hash on {platform.system()} with Python {platform.python_version()}: {hash_value}")

    def test_floating_point_accuracy(self):
        data = {"float1": 0.1, "float2": 0.2, "float_sum": 0.1 + 0.2}
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(data, file)

        initial_hash = hash_file(self.pickle_filename)
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(loaded_data, file)
        final_hash = hash_file(self.pickle_filename)
        self.assertEqual(initial_hash, final_hash)

    def test_recursive_data_structures(self):
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(self.recursive_data, file)

        initial_hash = hash_file(self.pickle_filename)
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(loaded_data, file)
        final_hash = hash_file(self.pickle_filename)
        self.assertEqual(initial_hash, final_hash)

    def test_various_data_types(self):
        types_data = {
            "none": None,
            "bool": True,
            "complex": complex(1, 2),
            "bytes": b"bytes",
            "bytearray": bytearray(b"bytes"),
            "memoryview": memoryview(b"bytes").tobytes(),
            "frozenset": frozenset([1, 2, 3])
        }
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(types_data, file)

        initial_hash = hash_file(self.pickle_filename)
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(loaded_data, file)
        final_hash = hash_file(self.pickle_filename)
        self.assertEqual(initial_hash, final_hash)

if __name__ == '__main__':
    unittest.main()

