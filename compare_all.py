import glob
import os
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def read_hash_file(filepath):
    """Read hash values from a file and return a dictionary."""
    hash_dict = {}
    with open(filepath, 'r') as file:
        print(filepath + "\n")
        for line in file:
            data_name, hash_value = line.strip().split(": ")
            hash_dict[data_name] = hash_value
    return hash_dict

def compare_hash_files(pattern):
    """Compare hash files matching the given pattern."""
    hash_files = glob.glob(pattern)
    hash_contents = {}

    for hash_file in hash_files:
        hash_contents[os.path.basename(hash_file)] = read_hash_file(hash_file)

    all_match = True
    data_types = set()
    
    for hash_dict in hash_contents.values():
        data_types.update(hash_dict.keys())
    
    for data_name in data_types:
        hash_values = {filename: hashes.get(data_name) for filename, hashes in hash_contents.items()}
        unique_hashes = set(hash_values.values())
        
        if len(unique_hashes) == 1:
            print(Fore.GREEN + f"All hash values for {data_name} match: {unique_hashes.pop()}")
        else:
            all_match = False
            print(Fore.RED + f"Hashes for {data_name} do not match:")
            for filename, hash_value in hash_values.items():
                print(Fore.RED + f"{filename}: {hash_value}")

    return all_match

if __name__ == '__main__':
    pattern = "hash_*.txt"
    all_match = compare_hash_files(pattern)

    if all_match:
        print(Fore.GREEN + "Verification successful: all hashes match.")
    else:
        print(Fore.RED + "Verification failed: there are mismatches in the hash values.")

