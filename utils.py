import hashlib

# Returns the SHA-256 hash of the file passed into it
def hash_file(filename):
    # make a hash object
    h = hashlib.sha256()

    # open file for reading in binary mode
    with open(filename, 'rb') as file:
        chunk = 0
        while chunk != b'':
            # read 1024
            chunk = file.read(1024)
            h.update(chunk)

    # return
    return h.hexdigest()
