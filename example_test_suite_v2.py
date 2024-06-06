import unittest
import pickle
import os
import platform
from compare_hashes import hash_file
from colorama import init, Fore, Style
import glob
from decimal import Decimal, getcontext
import array
from threading import Thread
import locale
from pathlib import Path
import time
import ctypes
#import resource

# Initialize colorama
init(autoreset=True)

# Define CustomObject at the module level
class CustomObject:
    def __init__(self, value):
        self.value = value

    def __getstate__(self):
        # Custom method to control what gets serialized
        state = self.__dict__.copy()
        state['value'] *= 2  # Just an example of manipulating the state
        return state

    def __setstate__(self, state):
        # Custom method to control how the object is restored
        state['value'] /= 2  # Restore original state
        self.__dict__.update(state)

class PickleTestBase(unittest.TestCase):

    def setUp(self):
        self.pickle_filename = "test_pickle.pkl"
<<<<<<< HEAD
        self.hash_file_path = f"{platform.system()}/hash_{platform.system()}_{platform.python_version()}.txt"
=======
        arch = platform.architecture()[0]
        if arch == "32bit":
            self.hash_file_path = f"hash_{platform.system()}_{platform.python_version()}_32bit.txt"
        else:
            self.hash_file_path = f"hash_{platform.system()}_{platform.python_version()}.txt"

>>>>>>> origin/Fritolf-Super

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
        self.write_to_file("Original data", final_hash)

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
        self.write_to_file("fp_accuracy", final_hash)

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
        self.write_to_file("Recursive_data", final_hash)

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
        self.write_to_file("Extended_data", final_hash)
    
    def test_dynamic_code_execution(self):
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
            self.write_to_file("Dynamic_code", final_hash)
        
    def test_high_precision_decimal_serialization(self):
        print(Fore.CYAN + "\nRunning test_high_precision_decimal_serialization...")

        # Using a high-precision Decimal constant
        high_precision_decimal = Decimal('0.12345678901234567890123456789012345678901234567890')

        # Serialize data and hash
        initial_hash = self.serialize_and_hash(high_precision_decimal)
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
        print(Fore.GREEN + "High precision decimal serialization test passed. Hashes match.")

        # Save to file
        self.write_to_file("high_precision_decimal", final_hash)

    def test_system_specific_types(self):
        print(Fore.CYAN + "\nRunning test_system_specific_types...")

        # Create an array of integers
        int_array = array.array('i', [1, 2, 3, 4])

        # Serialize data and hash
        initial_hash = self.serialize_and_hash(int_array)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserialize and serialize again
        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        # Get hash of the re-serialized file
        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        # Check if both hashes are the same
        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "System-specific type serialization test passed. Hashes match.")

        # Save to file
        self.write_to_file("system_specific_types", final_hash)

    def test_large_data_structures(self):
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

        # Check if both hashes are the same
        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Meta classes and dynamic class creation test passed. Hashes match.")

        # Save to file
        self.write_to_file("meta_classes_dynamic_creation", final_hash)

    def test_endianess_effect_on_serialization(self):
        print(Fore.CYAN + "\nRunning test_endianess_effect_on_serialization...")

        # Create an array of shorts, which will have a clear endianess order
        endian_sensitive_data = array.array('h', [0x1234, 0x5678])

        initial_hash = self.serialize_and_hash(endian_sensitive_data)
        print(Fore.GREEN + f"Final hash: {initial_hash}")

        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Endianess serialization test passed. Hashes match.")

        self.write_to_file("endianess_effect", final_hash)

    def test_function_memory_address(self):
        print(Fore.CYAN + "\nRunning test_function_memory_address...")

        # Use the named function instead of a lambda
        func = increment_func

        initial_hash = self.serialize_and_hash(func)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserialize and serialize again
        print(Fore.BLUE + "Deserializing and re-serializing data...")
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        # Check if both hashes are the same
        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Function memory address test passed. Hashes match.")

        # Save to file
        self.write_to_file("function_memory_address", final_hash)

<<<<<<< HEAD
    def test_custom_object_serialization(self):
        """Test serialization of CustomObject."""

        print(Fore.CYAN + "\nRunning custom_object...")

        data = CustomObject(10)
        initial_hash = self.serialize_and_hash(data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

=======
    def run_pickle_operations(self, data, results, index):
        results[index] = self.serialize_and_hash(data)

    def test_thread_safety_in_serialization(self):
        print(Fore.CYAN + "\nRunning test_thread_safety_in_serialization...")
        num_threads = 10
        threads = []
        results = [None] * num_threads

        # Launch multiple threads to perform pickling
        for i in range(num_threads):
            thread = Thread(target=self.run_pickle_operations, args=(self.data, results, i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Verify that all threads produced the same hash
        first_hash = results[0]
        for i in range(1, num_threads):
            self.compare_hashes(first_hash, results[i])

        print(Fore.GREEN + "All thread serialization results match.")
        self.write_to_file("thread_safety", first_hash)

    def test_locale_sensitivity(self):
        print(Fore.CYAN + "\nRunning test_locale_sensitivity...")
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        us_hash = self.serialize_and_hash(self.data)

        locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
        de_hash = self.serialize_and_hash(self.data)

        print(Fore.GREEN + f"US locale hash: {us_hash}")
        print(Fore.GREEN + f"German locale hash: {de_hash}")

        self.compare_hashes(us_hash, de_hash)
        print(Fore.GREEN + "Locale serialization test passed.")
        self.write_to_file("locale_sensitivity", us_hash)

    def test_filesystem_path_serialization(self):
        print(Fore.CYAN + "\nRunning test_filesystem_path_serialization...")
        # Using a relative path to avoid OS-specific root directories
        path = Path("path/to/resource")
        initial_hash = self.serialize_and_hash(path)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserialize and serialize again
>>>>>>> origin/Fritolf-Super
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
<<<<<<< HEAD
        print(Fore.GREEN + "Custom object code execution test passed. Hashes match.")

        # Save to file
        self.write_to_file("Custom_object", final_hash)


    def test_dynamic_code_execution(self):
        print(Fore.CYAN + "\nRunning test_dynamic_code_execution...")

        class EvalObject:
            def __reduce__(self):
                return (eval, ("1 + 2",))

        data = EvalObject()

        initial_hash = self.serialize_and_hash(data)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

=======
        print(Fore.GREEN + "Filesystem path serialization test passed.")
        self.write_to_file("filesystem_paths", initial_hash)

    def test_line_endings_serialization(self):
        print(Fore.CYAN + "\nRunning test_line_endings_serialization...")
        # Standardize on Unix line endings for the test
        text = "Hello\nWorld"

        initial_hash = self.serialize_and_hash(text)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserialize and serialize again
>>>>>>> origin/Fritolf-Super
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

<<<<<<< HEAD
        try:
            self.compare_hashes(initial_hash, final_hash)
            print(Fore.GREEN + "Dynamic code execution test passed. Hashes match.")
        finally:
            self.write_to_file("Dynamic_code", final_hash)


=======
        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Line endings serialization test passed.")
        self.write_to_file("line_endings", initial_hash)

    def test_environment_variable_effect(self):
        print(Fore.CYAN + "\nRunning test_environment_variable_effect...")
        # Use a static dictionary to simulate environment variables
        env_vars = {"PATH": "/usr/bin:/bin", "HOME": "/home/user"}

        initial_hash = self.serialize_and_hash(env_vars)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserialize and serialize again
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Environment variable simulation test passed.")
        self.write_to_file("environment_variables", initial_hash)
        
### Differencing between 32-bit and 64-bit Python installations
    def test_ctypes_pointer_serialization(self):
        print(Fore.CYAN + "\nRunning test_ctypes_pointer_serialization...")
        int_array = (ctypes.c_int * 5)(*range(5))  # An array of integers

        initial_hash = self.serialize_and_hash(ctypes.addressof(int_array))
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Attempting to deserialize this will likely not work or give different results,
        # because raw pointers do not carry over meaningfully across different runs or systems.
        # We expect this to fail or behave inconsistently, which is what we're testing for.
        try:
            with open(self.pickle_filename, 'rb') as file:
                loaded_data = pickle.load(file)
            final_hash = self.serialize_and_hash(loaded_data)
            print(Fore.GREEN + f"Final hash: {final_hash}")
            self.compare_hashes(initial_hash, final_hash)
        except Exception as e:
            print(Fore.RED + f"Expected error during deserialization: {str(e)}")
            self.write_to_file("ctypes_memory", "Error")

        print(Fore.GREEN + "Ctypes pointer serialization test completed.")
        self.write_to_file("ctypes_pointers", initial_hash)

    def test_integer_limits(self):
        print(Fore.CYAN + "\nRunning test_integer_limits...")
        # Use a very large integer that will behave differently in 32-bit vs 64-bit Python
        large_integer = 2**31 - 1  # Maximum 32-bit signed integer value

        initial_hash = self.serialize_and_hash(large_integer)
        print(Fore.GREEN + f"Initial hash: {initial_hash}")

        # Deserialize and serialize again
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash: {final_hash}")

        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Integer limit test passed.")
        self.write_to_file("integer_limits", initial_hash)

        def test_pointer_size_serialization(self):
            print(Fore.CYAN + "\nRunning test_pointer_size_serialization...")

        # Create a simple object
        obj = object()
        # Get the memory address of the object, which is inherently a pointer
        obj_id = id(obj)

        # Serialize the numeric representation of the memory address
        initial_hash = self.serialize_and_hash(obj_id)
        print(Fore.GREEN + f"Initial hash of object id (memory address): {initial_hash}")

        # Deserialize and serialize again to verify consistency within the same Python instance
        with open(self.pickle_filename, 'rb') as file:
            loaded_data = pickle.load(file)

        final_hash = self.serialize_and_hash(loaded_data)
        print(Fore.GREEN + f"Final hash after deserialization: {final_hash}")

        # This test checks internal consistency but note that `id()` values are not guaranteed
        # to be the same across different runs or different Python installations
        self.compare_hashes(initial_hash, final_hash)
        print(Fore.GREEN + "Pointer size serialization test passed.")
        self.write_to_file("pointer_size", initial_hash)

        # Note to self or other developers: The hash values here reflect memory addresses and are
        # not expected to match across different Python installations (32-bit vs 64-bit), hence 
        # this test is primarily illustrative and cannot use `compare_hashes` across installations.
>>>>>>> origin/Fritolf-Super
if __name__ == '__main__':
    unittest.main()


# Define CustomObject at the module level
class CustomObject:
    def __init__(self, value):
        self.value = value

    def __getstate__(self):
        # Custom method to control what gets serialized
        state = self.__dict__.copy()
        state['value'] *= 2  # Just an example of manipulating the state
        return state

    def __setstate__(self, state):
        # Custom method to control how the object is restored
        state['value'] /= 2  # Restore original state
        self.__dict__.update(state)

# Create a meta class dynamically using the type function
Meta = type('Meta', (type,), {})
# Create a class dynamically with Meta as its metaclass
class MyClass(metaclass=Meta):
    def __init__(self, value):
        self.value = value
    
<<<<<<< HEAD
=======
def increment_func(x):
    return x + 1
>>>>>>> origin/Fritolf-Super
