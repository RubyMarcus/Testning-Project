import unittest
import pickle
import os
import platform
from compare_hashes import hash_file
from colorama import init, Fore, Style
import glob

# Initialize colorama
init(autoreset=True)

class PickleTestBase(unittest.TestCase):

    def setUp(self):
        self.pickle_filename = "test_pickle.pkl"
        self.hash_file_path = f"hash_{platform.system()}_{platform.python_version()}.txt"

    def tearDown(self):
        if os.path.exists(self.pickle_filename):
            os.remove(self.pickle_filename)

    def serialize_and_hash(self, data):
        """Serialize data and return its hash."""
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(data, file)
        return hash_file(self.pickle_filename)

    def write_to_file(self, final_hash): 
        with open(self.hash_file_path, 'a') as file:
            file.write(final_hash)
            

    def compare_hashes(self, initial_hash, final_hash):
        """Serialize data and return its hash."""
        self.assertEqual(initial_hash, final_hash, Fore.RED + "Hashes do not match!")


class TestPickleStability(PickleTestBase):
    """Tests for Pickle Stability."""

    def setUp(self):
        super().setUp()
        self.data = {
            "int": 123,
            "float": 123.456,
            "string": "test",
            "list": [1, 2, 3],
            "dict": {"key": "value"},
            "tuple": (1, 2, 3),
            "set": {1, 2, 3}
        }

        self.recursive_data = {}
        self.recursive_data["self"] = self.recursive_data

        self.extended_data = {
            "none": None,
            "bool": True,
            "complex": complex(1, 2),
            "bytes": b"bytes",
            "bytearray": bytearray(b"bytes"),
            "memoryview": memoryview(b"bytes").tobytes(),
            "frozenset": frozenset([1, 2, 3]),
            "builtin_constants": [None, True, False, Ellipsis, NotImplemented],
            "numbers": [123, 123.456, 1+2j],
            "strings": ["test", b"bytes", bytearray(b"bytes")],
            "collections": [(1, 2), [1, 2], {1, 2}, {"key": "value"}],
        }

    def test_pickle_stability(self):
        """Opts to test the pickling stability inside the environment."""

        # TODO: We are only testing on self.data, add more?

        print(Fore.CYAN + "\nRunning test_pickle_stability...")
    
        initial_hash = self.serialize_and_hash(self.data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserialize and serialize again
        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        # Get the hash of the re-serialized file
        final_hash = self.serialize_and_hash(loaded_data) 
        print(Fore.GREEN + f"Final hash: {final_hash}")

        # Check if both hashes are the same
        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Pickle stability test passed. Hashes match.")
        
        # Save to file
        self.write_to_file(final_hash)

    """
    def test_cross_environment_stability(self):
        print(Fore.CYAN + "\nRunning test_cross_environment_stability...")

        hash_file_path = f"hash_{platform.system()}_{platform.python_version()}.txt"

        for data_name, data in self.extended_data.items():
            print(Fore.BLUE + f"Testing {data_name}...!")
            initial_hash = self.serialize_and_hash(data)
            with open(hash_file_path, 'a') as file:
                file.write(f"{data_name}: {initial_hash")
            print(Fore.GREEN + f"{data_name} hash: {initial_hash}")
    """
    
    def test_floating_point_accuracy(self):
        print(Fore.CYAN + "\nRunning test_floating_point_accuracy...")
    
        # Float data
        data = {"float1": 0.1, "float2": 0.2, "float_sum": 0.1 + 0.2}

        # Serialize data and hash
        initial_hash = self.serialize_and_hash(data) 
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserializing and re-serializing data
        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        # Get hash of the re-serialized file    
        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        # Check if both hashes are the same
        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Floating point accuracy test passed. Hashes match.")

        # Save to file
        self.write_to_file(final_hash)

    def test_recursive_data_structures(self):
        print(Fore.CYAN + "\nRunning test_recursive_data_structures...")

        # Serialize data and hash
        initial_hash = self.serialize_and_hash(self.recursive_data) 
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserializing and re-serializing data
        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        # Get hash of the re-serialized file 
        final_hash = self.serialize_and_hash(loaded_data) 
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Recursive data structure test passed. Hashes match.")

        # Save to file
        self.write_to_file(final_hash)

    def test_various_data_types(self):
        print(Fore.CYAN + "\nRunning test_various_data_types...")

        # Serialize data and hash
        initial_hash = self.serialize_and_hash(self.extended_data) 
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserializing and re-serializing data
        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(self.extended_data) 
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Various data types test passed. Hashes match.")

        # Save to file
        self.write_to_file(final_hash)

if __name__ == '__main__':
    unittest.main()

