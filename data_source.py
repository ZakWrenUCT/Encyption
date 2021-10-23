
from time import sleep
from hat.accelgyro import getGyro
from hat.tempHumidity import getTemp
from hat.pressure import getPressure
import csv
from datetime import datetime

class DataSource:
    def get_column_names():
        return  ("Time", "MagX", "MagY", "MagZ", "AccX", "AccY", "AccZ", "GyroX", 
                "GyroY", "GyroZ", "Temp", "Pres", "Yaw", "Pitch", "Roll", "DCM1", "DCM2", 
                "DCM3", "DCM4", "DCM5", "DCM6", "DCM7", "DCM8", "DCM9", "MagNED1", "MagNED2", 
                "MagNED3", "AccNED1", "AccNED2", "ACCNED3")

    def next(self):
        return [0.0]*29

class CSVDataSource(DataSource):
    
    def __init__(self, filename):
        self.filename = filename
        self.current_line = 1
        self.lines = []
        with open(self.filename) as f:
            self.lines = f.readlines()[1:]
        self.length = len(self.lines)

    def next(self):
        line = [float(x) for x in self.lines[self.current_line % self.length].strip().split(" ")[1:] if x != "\n"]
        self.current_line += 1
        return line

class IMUDataSource(DataSource):
    # TODO: Implement fetching columns from IMU
    def __init__(self):
        pass

    def column_names():
        # TODO: Return column names in order
        pass

    def next(self):
        gyroVals = getGyro()
        tempVals = getTemp()
        pressureVals = getPressure()
        # print(gyroVals)
        results = []
        # add time
        results.append(str(datetime.utcnow()))
        # add magvals
        for i in range(0, len(gyroVals[0])):
            results.append(str(gyroVals[0][i]))
        # add accvals
        for i in range(0, len(gyroVals[1])):
            results.append(str(gyroVals[1][i]))
        # add gyrovals
        for i in range(0, len(gyroVals[2])):
            results.append(str(gyroVals[2][i]))
        # add temp
        results.append(str(tempVals))
        # add pressure
        results.append(str(pressureVals))
        # add yaw, pitch, raw
        for i in range(0, len(gyroVals[3])):
            results.append(str(gyroVals[3][i]))
        # print(results)
        return results

if __name__ == "__main__":
    data_source = CSVDataSource("sample_data.csv")
    print(data_source.next())