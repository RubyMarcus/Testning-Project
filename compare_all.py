import os
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def read_hash_file(filepath):
    """Read hash values from a file and return a dictionary."""
    hash_dict = {}
    with open(filepath, 'r') as file:
        for line in file:
            data_name, hash_value = line.strip().split(": ")
            hash_dict[data_name] = hash_value
    return hash_dict

def compare_hash_files(file_paths):
    """Compare corresponding hash files."""
    hash_contents = {}

    for path in file_paths:
        base_name = os.path.basename(path)
        version = "_".join(base_name.split("_")[2:])  # Extract version part of the filename
        folder = os.path.basename(os.path.dirname(path))
        if version not in hash_contents:
            hash_contents[version] = {}
        hash_contents[version][folder] = read_hash_file(path)

    all_match = True

    for version, folder_hashes in hash_contents.items():
        #print(f"Comparing version: {version} with folders: {list(folder_hashes.keys())}")
        if len(folder_hashes) == 3:  # Check if all three folders are present
            data_types = set()
            for hash_dict in folder_hashes.values():
                data_types.update(hash_dict.keys())

            for data_name in data_types:
                hash_values = {folder: hashes.get(data_name) for folder, hashes in folder_hashes.items()}
                unique_hashes = set(hash_values.values())

                # Log the values being compared for debugging
                # print(f"\nComparing {data_name} in {version}:")
                #for folder, hash_value in hash_values.items():
                    #print(f"{folder}: {hash_value}")

                if len(unique_hashes) == 1:
                    #print(Fore.GREEN + f"All hash values for {data_name} in {version} match: {unique_hashes.pop()}")                   
                    continue
                else:
                    all_match = False
                    print(Fore.RED + f"Hashes for {data_name} in {version} do not match:")
                    for folder, hash_value in hash_values.items():
                        print(Fore.RED + f"{folder}: {hash_value}")
        else:
            print(Fore.YELLOW + f"File version {version} is not present in all folders.")

    return all_match

def main():
    file_paths = [
        "Darwin/hash_Darwin_3.6.15.txt",
        "Darwin/hash_Darwin_3.7.17.txt",
        "Darwin/hash_Darwin_3.8.12.txt",
        "Darwin/hash_Darwin_3.9.7.txt",
        "Darwin/hash_Darwin_3.10.1.txt",
        "Darwin/hash_Darwin_3.11.9.txt",
        "Darwin/hash_Darwin_3.12.3.txt",
        "Linux/hash_Linux_3.6.15.txt",
        "Linux/hash_Linux_3.7.17.txt",
        "Linux/hash_Linux_3.8.12.txt",
        "Linux/hash_Linux_3.9.7.txt",
        "Linux/hash_Linux_3.10.1.txt",
        "Linux/hash_Linux_3.11.9.txt",
        "Linux/hash_Linux_3.12.3.txt",
        "Windows/hash_Windows_3.6.15.txt", # actually version 3.6.8 (latest version)
        "Windows/hash_Windows_3.7.17.txt", # actually version 3.7.8 (latest version)
        "Windows/hash_Windows_3.8.12.txt",
        "Windows/hash_Windows_3.9.7.txt",
        "Windows/hash_Windows_3.10.1.txt",
        "Windows/hash_Windows_3.11.9.txt",
        "Windows/hash_Windows_3.12.3.txt",
    ]

    all_match = compare_hash_files(file_paths)

    if all_match:
        print(Fore.GREEN + "Overall verification successful: all hashes match across all folders.")
    else:
        print(Fore.RED + "Overall verification failed: there are mismatches in the hash values.")

if __name__ == '__main__':
    main()

