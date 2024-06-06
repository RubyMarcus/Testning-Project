import unittest
import pickle
import os
import platform
from compare_hashes import hash_file  # Ensure this module is available
from colorama import init, Fore, Style
from decimal import Decimal
import array
from threading import Thread
import locale
from pathlib import Path
import ctypes

# Initialize colorama
init(autoreset=True)


class CustomObject:
    """Class to demonstrate custom serialization."""

    def __init__(self, value):
        self.value = value

    def __getstate__(self):
        """Control what gets serialized."""
        state = self.__dict__.copy()
        state['value'] *= 2
        return state

    def __setstate__(self, state):
        """Control how the object is restored."""
        state['value'] /= 2
        self.__dict__.update(state)


class PickleTestBase(unittest.TestCase):
    """Base class for pickle tests."""

    def setUp(self):
        self.pickle_filename = "test_pickle.pkl"

        system = platform.system()
        version = platform.python_version()
        if system == "Windows":
            arch = platform.architecture()[0]
            if arch == "32bit":
                system = "Windows32"
            else:
                system = "Windows"
            print(Fore.YELLOW + f"System: {system}")
        self.hash_file_path = f"{system}/hash_{system}_{version}.txt"

    def tearDown(self):
        if os.path.exists(self.pickle_filename):
            os.remove(self.pickle_filename)

    def serialize_and_hash(self, data):
        """Serialize data and return its hash."""
        with open(self.pickle_filename, 'wb') as file:
            pickle.dump(data, file)
        return hash_file(self.pickle_filename)

    def write_to_file(self, data_type, final_hash):
        """Write hash to file."""
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
            "numbers": [123, 123.456, 1+2j],
            "strings": ["test", b"bytes", bytearray(b"bytes")],
            "collections": [(1, 2), [1, 2], {1, 2}, {"key": "value"}],
        }

    # TODO: KEEP
    def test_standard_data(self):
        """Test the pickling stability of standard data types."""
        print(Fore.CYAN + "\nRunning test_standard_data...")

        initial_hash = self.serialize_and_hash(self.data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Pickle stability test passed. Hashes match.")

        self.write_to_file("Standard data", final_hash)

    # TODO: KEEP
    def test_floating_point_accuracy(self):
        """Test the pickling accuracy of floating-point data."""
        print(Fore.CYAN + "\nRunning test_floating_point_accuracy...")

        data = {"float1": 0.1, "float2": 0.2, "float_sum": 0.1 + 0.2}

        initial_hash = self.serialize_and_hash(data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Floating point accuracy test passed. Hashes match.")

        self.write_to_file("Floating point accuracy", final_hash)

    # TODO: KEEP
    def test_high_precision_decimal_serialization(self):
        """Test the pickling of high-precision Decimal data."""
        print(Fore.CYAN + "\nRunning test_high_precision_decimal_serialization...")

        high_precision_decimal = Decimal('0.12345678901234567890123456789012345678901234567890')

        initial_hash = self.serialize_and_hash(high_precision_decimal)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "High precision decimal serialization test passed. Hashes match.")

        self.write_to_file("High precision decimal", final_hash)

    # TODO: KEEP
    def test_recursive_data_structures(self):
        """Test the pickling of recursive data structures."""
        print(Fore.CYAN + "\nRunning test_recursive_data_structures...")

        initial_hash = self.serialize_and_hash(self.recursive_data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Recursive data structure test passed. Hashes match.")

        self.write_to_file("Recursive data", final_hash)

    # TODO: KEEP
    def test_various_data_types(self):
        """Test the pickling of various data types."""
        print(Fore.CYAN + "\nRunning test_various_data_types...")

        initial_hash = self.serialize_and_hash(self.extended_data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(self.extended_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Various data types test passed. Hashes match.")

        self.write_to_file("Extended data", final_hash)

    # TODO: KEEP
    def test_dynamic_code_execution(self):
        """Test the pickling of dynamically executed code."""
        print(Fore.CYAN + "\nRunning test_dynamic_code_execution...")

        class EvalObject:
            def __reduce__(self):
                return (eval, ("1 + 2",))

        data = EvalObject()

        initial_hash = self.serialize_and_hash(data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        try:
            self.compare_hashes(initial_hash, final_hash)
            print(Fore.GREEN + "Dynamic code execution test passed. Hashes match.")
        finally:
            self.write_to_file("Dynamic code", final_hash)

    # TODO: KEEP
    def test_system_specific_types(self):
        """Test the pickling of system-specific types."""
        print(Fore.CYAN + "\nRunning test_system_specific_types...")

        int_array = array.array('i', [1, 2, 3, 4])

        initial_hash = self.serialize_and_hash(int_array)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "System-specific type serialization test passed. Hashes match.")

        self.write_to_file("System specific types", final_hash)

    # TODO: KEEP
    def test_large_data_structures(self):
        """Test the pickling of large data structures."""
        print(Fore.CYAN + "\nRunning test_large_data_structures...")

        large_data = {'key': list(range(1000000))}

        initial_hash = self.serialize_and_hash(large_data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Large data structures test passed. Hashes match.")

        self.write_to_file("Large data", final_hash)

    # TODO: KEEP
    def test_meta_classes_and_dynamic_creation(self):
        """Test the pickling of dynamically created classes with metaclasses."""
        print(Fore.CYAN + "\nRunning test_meta_classes_and_dynamic_creation...")

        data = MyClass(42)
        initial_hash = self.serialize_and_hash(data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Meta classes and dynamic class creation test passed. Hashes match.")

        self.write_to_file("Meta classes dynamic creation", final_hash)

    # TODO: KEEP
    def test_endianess_effect_on_serialization(self):
        """Test the effect of endianess on serialization."""
        print(Fore.CYAN + "\nRunning test_endianess_effect_on_serialization...")

        endian_sensitive_data = array.array('h', [0x1234, 0x5678])

        initial_hash = self.serialize_and_hash(endian_sensitive_data)
        print(Fore.GREEN + f"Final hash: {initial_hash}")

        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Endianess serialization test passed. Hashes match.")

        self.write_to_file("Endianess effect", final_hash)

    # TODO: KEEP
    def test_function_memory_address(self):
        """Test the pickling of function memory addresses."""
        print(Fore.CYAN + "\nRunning test_function_memory_address...")

        func = increment_func

        initial_hash = self.serialize_and_hash(func)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Function memory address test passed. Hashes match.")

        self.write_to_file("Function memory address", final_hash)

    # TODO: KEEP
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

        self.write_to_file("Custom object", final_hash)

    # TODO: HOLD
    def run_pickle_operations(self, data, results, index):
        results[index] = self.serialize_and_hash(data)

    # TODO: HOLD
    def test_thread_safety_in_serialization(self):
        """Test thread safety during serialization."""
        print(Fore.CYAN + "\nRunning test_thread_safety_in_serialization...")
        num_threads = 10
        threads = []
        results = [None] * num_threads

        for i in range(num_threads):
            thread = Thread(target=self.run_pickle_operations, args=(self.data, results, i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        first_hash = results[0]
        for i in range(1, num_threads):
            self.compare_hashes(first_hash, results[i])

        print(Fore.GREEN + "All thread serialization results match.")
        self.write_to_file("Thread safety", first_hash)
    
    # TODO: KEEP
    def test_locale_sensitivity(self):
        """Test the sensitivity of serialization to locale changes."""
        print(Fore.CYAN + "\nRunning test_locale_sensitivity...")
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        us_hash = self.serialize_and_hash(self.data)

        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
        de_hash = self.serialize_and_hash(self.data)

        print(Fore.GREEN + f"US locale hash: {us_hash}")
        print(Fore.GREEN + f"German locale hash: {de_hash}")

        self.compare_hashes(us_hash, de_hash)
        print(Fore.GREEN + "Locale serialization test passed.")
        self.write_to_file("Locale sensitivity", us_hash)

    # TODO: KEEP
    def test_filesystem_path_serialization(self):
        """Test the serialization of filesystem paths."""
        print(Fore.CYAN + "\nRunning test_filesystem_path_serialization...")

        path = Path("path/to/resource")
        initial_hash = self.serialize_and_hash(path)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Filesystem path serialization test passed. Hashes match.")

        self.write_to_file("Filesystem path", final_hash)
    
    # TODO: KEEP
    def test_line_endings_serialization(self):
        """Test the serialization of text with different line endings."""
        print(Fore.CYAN + "\nRunning test_line_endings_serialization...")

        text = "Hello\nWorld"

        initial_hash = self.serialize_and_hash(text)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Line endings serialization test passed. Hashes match.")

        self.write_to_file("Line endings", initial_hash)

    # TODO: 
    def test_environment_variable_effect(self):
        """Test the effect of environment variables on serialization."""
        print(Fore.CYAN + "\nRunning test_environment_variable_effect...")

        env_vars = {"PATH": "/usr/bin:/bin", "HOME": "/home/user"}

        initial_hash = self.serialize_and_hash(env_vars)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Environment variable simulation test passed.")
        self.write_to_file("Environment variables", initial_hash)

    def test_ctypes_pointer_serialization(self):
        """Test the serialization of ctypes pointers."""
        print(Fore.CYAN + "\nRunning test_ctypes_pointer_serialization...")
        int_array = (ctypes.c_int * 5)(*range(5))

        initial_hash = self.serialize_and_hash(ctypes.addressof(int_array))
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        try:
            with open(self.pickle_filename, 'rb') as file:
                loaded_data = pickle.load(file)
            final_hash = self.serialize_and_hash(loaded_data)
            print(Fore.GREEN + f"Final hash: {final_hash}")
            self.compare_hashes(initial_hash, final_hash)
        except Exception as e:
            print(Fore.RED + f"Expected error during deserialization: {str(e)}")
            self.write_to_file("Ctypes memory", "Error")

        print(Fore.GREEN + "Ctypes pointer serialization test completed.")
        self.write_to_file("Ctypes pointers", initial_hash)

    def test_integer_limits(self):
        """Test the serialization of integers at the limits of their size."""
        print(Fore.CYAN + "\nRunning test_integer_limits...")
        large_integer = 2**31 - 1

        initial_hash = self.serialize_and_hash(large_integer)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Integer limit test passed.")
        self.write_to_file("Integer limits", initial_hash)

    def test_pointer_size_serialization(self):
        """Test the serialization of object memory addresses."""
        print(Fore.CYAN + "\nRunning test_pointer_size_serialization...")

        obj = object()
        obj_id = id(obj)

        initial_hash = self.serialize_and_hash(obj_id)
        print(Fore.GREEN + f"Initial hash of object id (memory address): {initial_hash}")

        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash after deserialization: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Pointer size serialization test passed.")
        self.write_to_file("Pointer size", initial_hash)


class MyClass(metaclass=type('Meta', (type,), {})):
    """Example class with dynamic metaclass."""

    def __init__(self, value):
        self.value = value


def increment_func(x):
    """Example function for testing function serialization."""
    return x + 1


if __name__ == '__main__':
    unittest.main()

