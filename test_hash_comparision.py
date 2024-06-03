import glob
import unittest

class TestHashComparison(unittest.TestCase):

    def test_hash_comparison_across_environments(self):
        hash_files = glob.glob("hash_*.txt")
        hash_values = []

        for hash_file in hash_files:
            with open(hash_file, 'r') as file:
                hash_values.append(file.read().strip())

        # Ensure all hash values are the same
        unique_hashes = set(hash_values)
        self.assertEqual(len(unique_hashes), 1, f"Hashes do not match: {unique_hashes}")
        print(f"All hash values match: {unique_hashes.pop()}")
