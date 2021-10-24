from imu_data_source import IMUDataSource
from test_cross_platform import benchmark_processing
from time import sleep

if __name__ == "__main__":
    while(True):
        inputObj = input("Enter b for benchmark, or r for readings:\n")
        if inputObj == "b":
            benchmark_processing()
        elif inputObj == "r":
            k = 0
            while k < 25:
                data_source = IMUDataSource()
                data = ",".join(data_source.next())
                print(data)
                sleep(1)
                k += 1
        else:
            print("invalid command")
