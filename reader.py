import os
from encryption import Encryption
from compression import Compression

"""
Decrypts and decompresses file
"""
def readfile(e: Encryption, c: Compression, in_filename, out_filename):
    compressed_filename = in_filename.split(".enc")[0]
    e.decrypt_file(in_filename, compressed_filename)
    c.decompress_file(compressed_filename, out_filename)
    os.remove(compressed_filename)

if __name__ == "__main__":
    e = Encryption()
    c = Compression()

    in_dir = os.path.join("batches")
    out_dir = os.path.join(in_dir, "output")

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    files = [x for x in os.listdir(in_dir) if x.endswith(".enc")]
    for file in files:
        csv_filename = os.path.join(out_dir, file.split(".enc")[0]).split(".gz")[0]
        print(file)
        readfile(e, c, os.path.join(in_dir, file), csv_filename)