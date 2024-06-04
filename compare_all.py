import glob
import os
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def read_hash_file(filepath):
    """Read the entire hash from a file."""
    with open(filepath, 'r') as file:
        return file.read().strip()

def compare_hash_files(pattern):
    """Compare hash files matching the given pattern."""
    hash_files = glob.glob(pattern)
    hash_contents = {}

    for hash_file in hash_files:
        hash_contents[os.path.basename(hash_file)] = read_hash_file(hash_file)

    unique_hashes = set(hash_contents.values())
    if len(unique_hashes) == 1:
        print(Fore.GREEN + "All hash values match across environments.")
        return True
    else:
        print(Fore.RED + "Hashes do not match across environments:")
        for filename, hash_value in hash_contents.items():
            print(Fore.RED + f"{filename}: {hash_value}")
        return False

if __name__ == '__main__':
    pattern = "hash_*.txt"
    all_match = compare_hash_files(pattern)

    if all_match:
        print(Fore.GREEN + "Verification successful: all hashes match.")
    else:
        print(Fore.RED + "Verification failed: there are mismatches in the hash values.")

