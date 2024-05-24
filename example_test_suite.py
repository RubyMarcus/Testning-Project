import hashlib
import pickle
import os
import platform
import logging
import sys

# Custom class for testing
class CustomClass:
    def __init__(self,value):
        self.value = value

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)

def sample_function():
    return "This is a sample function"

# Generator for testing
def sample_generator():
    yield from range(10)

# Sample lambda function
sample_lambda = lambda x: x + 1



def compute_pickle_hash(obj):
    try:
        pickled_data = pickle.dumps(obj)
        return hashlib.sha256(pickled_data).hexdigest()
    except Exception as e:
        #logging.error(f"Error pickling object {obj}: {e}")
        return str(e)

def test_pickling():
    test_cases = [
        # Basic Data Types
        None, True, False, Ellipsis, NotImplemented, 123, 45.67, complex(2, 3), "A string", b"bytes", bytearray(b"bytearray"),
        # Collections
        (1, 2, 3), [1, 2, 3], {1, 2, 3}, {"key": "value", "num": 42},
        [i for i in range(1000)], {i: str(i) for i in range(1000)},
        # Function and Classes
        sample_function, CustomClass(42), sample_lambda,
        # Advanced Objects
        sample_generator(), iter([1, 2, 3]), zip([1, 2, 3], ['a', 'b', 'c']),
        # Custom and Recursive Objects
        {"self": None}
    ]

    # Add circular reference
    test_cases[-1]["self"] = test_cases[-1]

    results = {}
    for i, test_case in enumerate(test_cases):
        hash_value = compute_pickle_hash(test_case)
        results[f"Test case {i + 1}"] = hash_value

    return results

if __name__ == "__main__":
    results = test_pickling()
    system_info = {
        "os": os.name,
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "python_version": sys.version
    }

    print("System Info:", system_info)
    print("Pickle Hashes", results)

    with open('hashes_run1.txt', 'w') as f:
        for test_case, hash_value in results.items():
            f.write(f"{test_case}: {hash_value}\n")


