import unittest
import pickle
import os
import platform
from compare_hashes import hash_file
from colorama import init, Fore
import array
from decimal import Decimal

# Initialize colorama
init(autoreset=True)

class CustomObject:
    def __init__(self, value):
        self.value = value

    def __getstate__(self):
        state = self.__dict__.copy()
        state['value'] *= 2
        return state

    def __setstate__(self, state):
        state['value'] /= 2
        self.__dict__.update(state)


class PickleTestBase(unittest.TestCase):
    def setUp(self):
        self.pickle_filename = "test_pickle.pkl"
        self.hash_file_path = f"{platform.system()}/hash_{platform.system()}_{platform.python_version()}.txt"

    def tearDown(self):
        if os.path.exists(self.pickle_filename):
            os.remove(self.pickle_filename)

    def serialize_and_hash(self, data):
        """Serialize data and return its hash."""
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(data, file)
        return hash_file(self.pickle_filename)

    def write_to_file(self, data_type, final_hash):
        with open(self.hash_file_path, 'a') as file:
            file.write(f"{data_type}: {final_hash}\n")

    def compare_hashes(self, initial_hash, final_hash):
        """Compare initial and final hashes."""
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
            "numbers": [123, 123.456, 1 + 2j],
            "strings": ["test", b"bytes", bytearray(b"bytes")],
            "collections": [(1, 2), [1, 2], {1, 2}, {"key": "value"}],
        }

    def test_original_data(self):
        """Test the pickling stability inside the environment."""
        print(Fore.CYAN + "\nRunning test_pickle_stability...")

        initial_hash = self.serialize_and_hash(self.data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserialize and serialize again
        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        # Check if both hashes are the same
        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Pickle stability test passed. Hashes match.")

        # Save to file
        self.write_to_file("Original data", final_hash)

    def test_floating_point_accuracy(self):
        print(Fore.CYAN + "\nRunning test_floating_point_accuracy...")

        data = {"float1": 0.1, "float2": 0.2, "float_sum": 0.1 + 0.2}

        initial_hash = self.serialize_and_hash(data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserialize and serialize again
        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        # Check if both hashes are the same
        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Floating point accuracy test passed. Hashes match.")

        # Save to file
        self.write_to_file("fp_accuracy", final_hash)

    def test_recursive_data_structures(self):
        print(Fore.CYAN + "\nRunning test_recursive_data_structures...")

        initial_hash = self.serialize_and_hash(self.recursive_data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserialize and serialize again
        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Recursive data structure test passed. Hashes match.")

        # Save to file
        self.write_to_file("Recursive_data", final_hash)

    def test_various_data_types(self):
        print(Fore.CYAN + "\nRunning test_various_data_types...")

        initial_hash = self.serialize_and_hash(self.extended_data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserialize and serialize again
        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(self.extended_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Various data types test passed. Hashes match.")

        # Save to file
        self.write_to_file("Extended_data", final_hash)

    def test_dynamic_code_execution(self):
        print(Fore.CYAN + "\nRunning test_dynamic_code_execution...")

        class EvalObject:
            def __reduce__(self):
                return eval, ("1 + 2",)

        data = EvalObject()

        initial_hash = self.serialize_and_hash(data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserialize and serialize again
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        try:
            self.compare_hashes(initial_hash, final_hash)
            print(Fore.GREEN + "Dynamic code execution test passed. Hashes match.")
        finally:
            self.write_to_file("Dynamic_code", final_hash)

    def test_high_precision_decimal_serialization(self):
        print(Fore.CYAN + "\nRunning test_high_precision_decimal_serialization...")

        high_precision_decimal = Decimal('0.12345678901234567890123456789012345678901234567890')

        initial_hash = self.serialize_and_hash(high_precision_decimal)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserialize and serialize again
        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "High precision decimal serialization test passed. Hashes match.")

        self.write_to_file("high_precision_decimal", final_hash)

    def test_system_specific_types(self):
        print(Fore.CYAN + "\nRunning test_system_specific_types...")

        int_array = array.array('i', [1, 2, 3, 4])

        initial_hash = self.serialize_and_hash(int_array)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserialize and serialize again
        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "System-specific type serialization test passed. Hashes match.")

        self.write_to_file("system_specific_types", final_hash)

    def test_large_data_structures(self):
        print(Fore.CYAN + "\nRunning test_large_data_structures...")

        large_data = {'key': list(range(1000000))}

        initial_hash = self.serialize_and_hash(large_data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserialize and serialize again
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Large data structures test passed. Hashes match.")

        self.write_to_file("Large_data", final_hash)

    def test_meta_classes_and_dynamic_creation(self):
        print(Fore.CYAN + "\nRunning test_meta_classes_and_dynamic_creation...")

        data = MyClass(42)
        initial_hash = self.serialize_and_hash(data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserialize and serialize again
        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Meta classes and dynamic class creation test passed. Hashes match.")

        self.write_to_file("meta_classes_dynamic_creation", final_hash)

    def test_endianess_effect_on_serialization(self):
        print(Fore.CYAN + "\nRunning test_endianess_effect_on_serialization...")

        endian_sensitive_data = array.array('h', [0x1234, 0x5678])

        initial_hash = self.serialize_and_hash(endian_sensitive_data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Endianess serialization test passed. Hashes match.")

        self.write_to_file("endianess_effect", final_hash)

    """ hmm, we can't pickle lambda functions
    def test_function_memory_address(self):
        print(Fore.CYAN + "\nRunning test_function_memory_address...")

        func = lambda x: x + 1

        initial_hash = self.serialize_and_hash(func)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Function memory address test passed. Hashes match.")

        self.write_to_file("function_memory_address", final_hash)
    """

    def test_custom_object_serialization(self):
        """Test serialization of CustomObject."""
        print(Fore.CYAN + "\nRunning custom_object...")

        data = CustomObject(10)
        initial_hash = self.serialize_and_hash(data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Custom object serialization test passed. Hashes match.")

        self.write_to_file("Custom_object", final_hash)


class MyClass(metaclass=type('Meta', (type,), {})):
    def __init__(self, value):
        self.value = value


if __name__ == '__main__':
    unittest.main()

