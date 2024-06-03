import unittest
import pickle
import os
import platform
from compare_hashes import hash_file
from colorama import init, Fore, Style
import glob

# Initialize colorama
init(autoreset=True)

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

        self.hash_filename = f"hash_{platform.system()}_{platform.python_version()}.txt"

    def tearDown(self):
        if os.path.exists(self.pickle_filename):
            os.remove(self.pickle_filename)

    def test_pickle_stability(self):
        print(Fore.CYAN + "\nRunning test_pickle_stability...")

        # Serialize the data
        print(Fore.BLUE + "Serializing data...")
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(self.data, file)

        # Get the hash of the serialized file
        initial_hash = hash_file(self.pickle_filename)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserialize and serialize again
        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(loaded_data, file)

        # Get the hash of the re-serialized file
        final_hash = hash_file(self.pickle_filename)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        # Check if both hashes are the same
        self.assertEqual(initial_hash, final_hash, Fore.RED + "Hashes do not match! Pickle stability test failed.")
        print(Fore.GREEN + "Pickle stability test passed. Hashes match.")

    def test_cross_environment_stability(self):
        print(Fore.CYAN + "\nRunning test_cross_environment_stability...")

        # Serialize the data
        print(Fore.BLUE + "Serializing data...")
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(self.data, file)

        hash_value = hash_file(self.pickle_filename)

        
        # Write the hash value to a file
        with open(self.hash_filename, 'w') as test_hash_comparison:
            test_hash_comparison.write(hash_value)

        print(Fore.GREEN + f"Hash on {platform.system()} with Python {platform.python_version()}: {hash_value}")

    def test_floating_point_accuracy(self):
        print(Fore.CYAN + "\nRunning test_floating_point_accuracy...")

        data = {"float1": 0.1, "float2": 0.2, "float_sum": 0.1 + 0.2}
        print(Fore.BLUE + "Serializing data with floating-point numbers...")
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(data, file)

        initial_hash = hash_file(self.pickle_filename)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(loaded_data, file)

        final_hash = hash_file(self.pickle_filename)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.assertEqual(initial_hash, final_hash, Fore.RED + "Hashes do not match! Floating point accuracy test failed.")
        print(Fore.GREEN + "Floating point accuracy test passed. Hashes match.")

    def test_recursive_data_structures(self):
        print(Fore.CYAN + "\nRunning test_recursive_data_structures...")

        print(Fore.BLUE + "Serializing recursive data structure...")
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(self.recursive_data, file)

        initial_hash = hash_file(self.pickle_filename)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(loaded_data, file)

        final_hash = hash_file(self.pickle_filename)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.assertEqual(initial_hash, final_hash, Fore.RED + "Hashes do not match! Recursive data structure test failed.")
        print(Fore.GREEN + "Recursive data structure test passed. Hashes match.")

    def test_various_data_types(self):
        print(Fore.CYAN + "\nRunning test_various_data_types...")

        types_data = {
            "none": None,
            "bool": True,
            "complex": complex(1, 2),
            "bytes": b"bytes",
            "bytearray": bytearray(b"bytes"),
            "memoryview": memoryview(b"bytes").tobytes(),
            "frozenset": frozenset([1, 2, 3])
        }
        print(Fore.BLUE + "Serializing various data types...")
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(types_data, file)

        initial_hash = hash_file(self.pickle_filename)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(loaded_data, file)

        final_hash = hash_file(self.pickle_filename)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.assertEqual(initial_hash, final_hash, Fore.RED + "Hashes do not match! Various data types test failed.")
        print(Fore.GREEN + "Various data types test passed. Hashes match.")

if __name__ == '__main__':
    unittest.main()

