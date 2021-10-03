import os
import subprocess

class Encryption:
    def __init__(self):
        pass

    def encrypt_file(self, in_filename, out_filename, password):
        subprocess.run(f"openssl enc -bf -a -salt -in \"{in_filename}\" -out \"{out_filename}\" -pass pass:{password}", shell=True)

    def decrypt_file(self, in_filename, out_filename, password):
        subprocess.run(f"openssl enc -bf -d -a -in \"{in_filename}\" -out \"{out_filename}\" -pass pass:{password}", shell=True)

if __name__ == "__main__":
    e = Encryption()
    e.encrypt_file("test.txt", "test.enc", "test")
    e.decrypt_file("test.enc", "test.decrypt", "test")