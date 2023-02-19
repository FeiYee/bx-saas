import hashlib


def get_file_md5(filename):
    m = hashlib.md5()
    with open(filename, 'rb') as fb:
        while True:
            data = fb.read(4096)
            if not data:
                break
            m.update(data)

    return m.hexdigest()

