import glob
import unittest
from collections import defaultdict
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

class TestHashComparison(unittest.TestCase):

    def test_hash_comparison_across_environments(self):
        hash_files = glob.glob("hash_Darwin*.txt")
        hash_dict = defaultdict(dict)

        # Read hash files and store values
        for hash_file in hash_files:
            print(Fore.BLUE + f"Reading file: {hash_file}")
            with open(hash_file, 'r') as file:
                for line in file:
                    data_type, hash_value = line.strip().split(": ")
                    python_version = hash_file.split('_')[2]  # Extract version from filename
                    hash_dict[data_type][python_version] = hash_value

        print(hash_dict)

        all_match = True

        # Compare hashes for each data type
        for data_type, version_hashes in hash_dict.items():
            print(Fore.BLUE + f"Comparing hashes for data type: {data_type}")
            hash_value_groups = defaultdict(list)
            for version, hash_value in version_hashes.items():
                hash_value_groups[hash_value].append(version)

            most_common_hash = max(hash_value_groups, key=lambda k: len(hash_value_groups[k]))
            unique_hashes = set(version_hashes.values())

            if len(unique_hashes) == 1:
                print(Fore.GREEN + f"All hash values for {data_type} match: {unique_hashes.pop()}")
            else:
                all_match = False
                print(Fore.RED + f"Hashes for {data_type} do not match:")
                for hash_value, versions in hash_value_groups.items():
                    color = Fore.GREEN if hash_value == most_common_hash else Fore.RED
                    for version in versions:
                        print(f"{color}  {version}: {hash_value}")

        self.assertTrue(all_match, "Not all hashes match across environments.")


if __name__ == '__main__':
    unittest.main()

