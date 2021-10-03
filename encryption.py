import os
import subprocess

class Encryption:
    def __init__(self, password=None):
        self.password = password or os.environ.get("PASSWORD", "pass")
        pass

    def encrypt_file(self, in_filename, out_filename):
        subprocess.run(f"openssl enc -bf -a -salt -in \"{in_filename}\" -out \"{out_filename}\" -pass pass:{self.password}", shell=True)

    def decrypt_file(self, in_filename, out_filename):
        subprocess.run(f"openssl enc -bf -d -a -in \"{in_filename}\" -out \"{out_filename}\" -pass pass:{self.password}", shell=True)

if __name__ == "__main__":
    e = Encryption()
    e.encrypt_file("test.txt", "test.enc")
    e.decrypt_file("test.enc", "test.decrypt")