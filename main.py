#!/usr/bin/env python3
import time
from datetime import datetime, timedelta
from typing import List
from data_source import CSVDataSource, IMUDataSource
import os
import csv
from encryption import Encryption
from compression import Compression

batch_dir = os.path.join("batches")

if not os.path.exists(batch_dir):
    os.makedirs(batch_dir)

def write_columns_to_csv(rows, column_names, filename):
    # column_names = ("Time", "MagX", "MagY", "MagZ", "AccX", "AccY", "AccZ", "GyroX", 
    # "GyroY", "GyroZ", "Temp", "Pres", "Yaw", "Pitch", "Roll", "DCM1", "DCM2", 
    # "DCM3", "DCM4", "DCM5", "DCM6", "DCM7", "DCM8", "DCM9", "MagNED1", "MagNED2", 
    # "MagNED3", "AccNED1", "AccNED2", "ACCNED3")
    
    with open(filename, "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(column_names)
        csvwriter.writerows(rows)
    

"""
Compress and encrypt all data files
"""
def process_batch(batch_rows: List[float], column_names: List[str], start_time: datetime, end_time: datetime, keep_intermediaries=False):
    csv_name = os.path.join(batch_dir, f"{start_time}-{end_time}.csv")
    print(csv_name)
    compressed_csv_name = f"{csv_name}.gz"
    encrypted_name = f"{compressed_csv_name}.enc"

    write_columns_to_csv(batch_rows, column_names, csv_name)
    
    c = Compression()
    c.compress_file(csv_name, compressed_csv_name)
    
    e = Encryption()
    e.encrypt_file(compressed_csv_name, out_filename=encrypted_name)

    if not keep_intermediaries:
        os.remove(csv_name)
        os.remove(compressed_csv_name)
    
    return encrypted_name

def main():

    last_batch_time = datetime.utcnow()
    batching_interval = timedelta(seconds=2)
    if os.environ.get("DEBUG", "false").lower() != "true":
        data_source = IMUDataSource()
    else:
        data_source = CSVDataSource("sample_data.csv")
    batch_rows = []

    while True:
        data = data_source.next()
        current_time = datetime.utcnow()
        data.insert(0, current_time)
        batch_rows.append(data)
        
        if current_time - last_batch_time > batching_interval:
            process_batch(batch_rows, data_source.get_column_names(), start_time=last_batch_time, end_time=current_time, keep_intermediaries=True)
            batch_rows = []
            last_batch_time = current_time
        
        print(current_time - last_batch_time)
        time.sleep(0.1)


if __name__ == "__main__":
    main()