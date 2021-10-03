import os
from encryption import Encryption
from compression import Compression

if __name__ == "__main__":
    e = Encryption()
    c = Compression()

    in_dir = os.path.join("batches")
    out_dir = os.path.join(in_dir, "output")

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    files = [x for x in os.listdir(in_dir) if x.endswith(".enc")]
    print(files)
    for file in files:
        compressed_filename = os.path.join(out_dir, file.split(".enc")[0])
        print(compressed_filename)
        csv_filename = compressed_filename.split(".gz")[0]
        print(csv_filename)
        
        e.decrypt_file(os.path.join(in_dir, file), compressed_filename, password="pass")
        c.decompress_file(compressed_filename, csv_filename)
        os.remove(compressed_filename)