import gzip
import shutil

class Compression:
    def __init__(self):
        pass

    def compress_file(self, in_filename, out_filename):
        with open(in_filename, 'rb') as f_in:
            with gzip.open(out_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    def decompress_file(self, in_filename, out_filename):
        with gzip.open(in_filename, 'r') as f_in:
            with open(out_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)


if __name__ == "__main__":
    c = Compression()
    c.compress_file("")