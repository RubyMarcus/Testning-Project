import hashlib

def hash_file(filename):
    """Returns the SHA-256 hash of the file passed into it"""
    h = hashlib.sha256()

    with open(filename, 'rb') as file:
        chunk = 0
        while chunk != b'':
            # read 1024
            chunk = file.read(1024)
            h.update(chunk)

    return h.hexdigest()
