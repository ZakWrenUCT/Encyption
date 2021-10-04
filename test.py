from datetime import datetime, timedelta
from data_source import CSVDataSource
from main import process_batch
from reader import readfile
from encryption import Encryption
from compression import Compression
from benchmarking import Benchmarking
import subprocess
import os


if __name__ == "__main__":
    current_time = datetime.utcnow()
    data_source = CSVDataSource("sample_data.csv")
    batch_rows = []

    for i in range(10):
        data = data_source.next()
        data.insert(0, current_time + timedelta(seconds=10*i))
        batch_rows.append(data)

    encrypted_filename = process_batch(
        batch_rows=batch_rows,
        start_time=current_time,
        end_time=current_time + timedelta(seconds=10*9),
        keep_intermediaries=True
    )

    print("Compression benchmark:")
    for i in range(10):
        Benchmarking.startlog()
        c = Compression()
        Benchmarking.endlogThrow()
    Benchmarking.startlog()
    c = Compression()
    Benchmarking.endlog()

    print("Encryption benchmark:\n")
    for i in range(10):
        Benchmarking.startlog()
        e = Encryption()
        Benchmarking.endlogThrow()
    Benchmarking.startlog()
    e = Encryption()
    Benchmarking.endlog()

    csv_filename = encrypted_filename.split(".gz.enc")[0]
    out_filename = os.path.join(
        "".join(csv_filename.split("/")[:-1]), "test.csv").replace(" ", "\ ")

    readfile(
        e, c,
        in_filename=encrypted_filename,
        out_filename=out_filename
    )

    print(f"diff \"{csv_filename}\" {out_filename}")
    process = subprocess.run(
        f"diff \"{csv_filename}\" {out_filename}", shell=True)
    if process.returncode == 0:
        print("Files match")
    else:
        print("Files don't match")
