
class DataSource:
    """
    returns (MagX, MagY, MagZ, AccX, AccY, AccZ, GyroX, 
    GyroY, GyroZ, Temp, Pres, Yaw, Pitch, Roll, DCM1, DCM2, 
    DCM3, DCM4, DCM5, DCM6, DCM7, DCM8, DCM9, MagNED1, MagNED2, 
    MagNED3, AccNED1, AccNED2, ACCNED3)
    """
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
    pass


if __name__ == "__main__":
    data_source = CSVDataSource("sample_data.csv")
    print(data_source.next())