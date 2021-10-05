from ast import Str
from datetime import datetime, timedelta
from data_source import CSVDataSource
from main import process_batch, write_columns_to_csv
from reader import readfile
from encryption import Encryption
from compression import Compression
from benchmarking import Benchmarking
import subprocess
import os

def test_overall():
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

    c = Compression()
    e = Encryption()

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

    oriSize = os.path.getsize(csv_filename)
    compSize = os.path.getsize(encrypted_filename)
    compRatio = str(round(oriSize/compSize, 2))+":1"
    print(compRatio)

def benchmark_compression():
    c = Compression()

    benchmarks = []

    for i in range(10):
        current_time = datetime.utcnow()
        data_source = CSVDataSource("sample_data.csv")
        batch_rows = []
        row_count = 10_000*i

        for i in range(row_count):
            data = data_source.next()
            data.insert(0, current_time + timedelta(seconds=0.1*i))
            batch_rows.append(data)
        
        write_columns_to_csv(batch_rows, "test.csv")
        
        in_filename = "test.csv"
        out_filename = f"{in_filename}.gz"
        data_duration = timedelta(seconds=0.1*row_count)
        print(f"Compressing {data_duration}'s worth of data")

        Benchmarking.startlog()
        c.compress_file(in_filename, out_filename)
        t = Benchmarking.endlog()

        oriSize = os.path.getsize(in_filename)
        compSize = os.path.getsize(out_filename)
        compRatio = str(round(oriSize/compSize, 2))+":1"
        print("Compression ratio:", compRatio)

        benchmarks.append((data_duration, t, compRatio))

        os.remove(in_filename)
        os.remove(out_filename)

        print("")

    print("data_duration,t,compRatio")
    for b in benchmarks:
        print(",".join([str(x) for x in b]))



def benchmark_processing():
    c = Compression()
    e = Encryption()

    benchmarks = []

    for i in range(10):
        current_time = datetime.utcnow()
        data_source = CSVDataSource("sample_data.csv")
        batch_rows = []
        row_count = 10_000*i

        for i in range(row_count):
            data = data_source.next()
            data.insert(0, current_time + timedelta(seconds=0.1*i))
            batch_rows.append(data)
        
        write_columns_to_csv(batch_rows, "test.csv")
        
        in_filename = "test.csv"
        out_filename = f"{in_filename}.gz"
        enc_filename = f"{out_filename}.enc"
        data_duration = timedelta(seconds=0.1*row_count)
        print(f"Compressing {data_duration}'s worth of data")

        Benchmarking.startlog()
        c.compress_file(in_filename, out_filename)
        t_compression = Benchmarking.endlog()

        Benchmarking.startlog()
        e.encrypt_file(out_filename, enc_filename)
        t_encryption = Benchmarking.endlog()

        Benchmarking.startlog()
        e.decrypt_file(enc_filename, out_filename)
        t_decryption = Benchmarking.endlog()

        Benchmarking.startlog()
        c.decompress_file(out_filename, in_filename)
        t_decompression = Benchmarking.endlog()

        oriSize = os.path.getsize(in_filename)
        compSize = os.path.getsize(out_filename)
        compRatio = str(round(oriSize/compSize, 2))
        print("Compression ratio:", compRatio)

        benchmarks.append((data_duration, t_compression, compRatio, t_encryption, t_decryption, t_decompression))

        os.remove(in_filename)
        os.remove(out_filename)
        # os.remove(enc_filename)

        print("")

        print("data_duration,t_compression,compRatio,t_encryption,t_decryption,t_decompression")
        for b in benchmarks:
            print(",".join([str(x) for x in b]))

if __name__ == "__main__":
    benchmark_processing()
