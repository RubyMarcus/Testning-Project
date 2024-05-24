def load_hashes(filename):
    hashes = {}
    with open(filename, 'r') as f:
        for line in f:
            test_case, hash_value = line.strip().split(': ')
            hashes[test_case] = hash_value
    return hashes

def compare_hashes(file1, file2):
    hashes1 = load_hashes(file1)
    hashes2 = load_hashes(file2)

    for test_case in hashes1:
        if test_case in hashes2:
            if hashes1[test_case] == hashes2[test_case]:
                print(f"{test_case}: MATCH")
            else:
                print(f"{test_case}: MISMATCH")
        else:
            print(f"{test_case}: NOT FOUND IN {file2}")

if __name__ == "__main__":
    compare_hashes('hashes_run1.txt', 'hashes_run2.txt')
