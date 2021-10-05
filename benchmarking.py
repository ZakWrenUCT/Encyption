from datetime import datetime, timedelta
from data_source import CSVDataSource
from main import process_batch
from reader import readfile
from encryption import Encryption
from compression import Compression
import subprocess
import os
from time import time, strftime, localtime
from datetime import timedelta


class Benchmarking:
    start = ''

    def secondsToStr(elapsed=None):
        if elapsed is None:
            return strftime("%Y-%m-%d %H:%M:%S", localtime())
        else:
            return str(timedelta(seconds=elapsed))

    def log(s, elapsed=None):
        line = "="*40
        print(line)
        print(Benchmarking.secondsToStr(), '-', s)
        if elapsed:
            print("Elapsed time:", elapsed)
        print(line)

    def startlog():
        global start
        start = time()
        # Benchmarking.log("Starting log")

    def endlog():
        global start
        end = time()
        elapsed = end-start
        Benchmarking.log("End Program", Benchmarking.secondsToStr(elapsed))
        return elapsed

    def endlogThrow():
        global start
        end = time()
        elapsed = end-start
