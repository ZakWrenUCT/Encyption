from time import sleep
from hat.accelgyro import getGyro, ICM20948
from hat.tempHumidity import getTemp
from hat.pressure import getPressure
import csv
from datetime import datetime
from data_source import DataSource

class IMUDataSource(DataSource):
    def __init__(self):
        self.icm20948 = ICM20948()

    def get_column_names():
        return ("Time", "MagX", "MagY", "MagZ", "AccX", "AccY", "AccZ", "GyroX",
                "GyroY", "GyroZ", "Temp", "Pres", "Yaw", "Pitch", "Roll")


    def next(self):
        gyroVals = getGyro(self.icm20948)
        tempVals = getTemp()
        pressureVals = getPressure()
        # print(gyroVals)
        results = []
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