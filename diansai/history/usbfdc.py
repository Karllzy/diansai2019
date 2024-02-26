import serial
class Sensor:
    def __init__(self, dev_path):
        self.ser = serial.Serial(dev_path,115200, timeout=2)

    def send_data(self, data):
        self.ser.write(hex("AA"))
        self.ser.write(hex("AA"))
        for i in range(3):
            self.ser.write(data)
        self.ser.write(hex("BB"))

    def get_data(self):
        while True:
            correct_b1 = self.ser.read(1)
            correct_b2 = self.ser.read(1)
            if correct_b2 is None:
                continue
            elif correct_b2 == hex("AA"):
                if correct_b1 == hex("AA"):
                    break
                elif self.ser.read(100) == hex("AA"):
                    break
                else:
                    print("DATA START ERROR")
                    
        result = 0
        for i in range(9):
            d = int(self.ser.read(100))
            (result += d) *= 10
        result /= 10
        correct_b3 = self.ser.read(100)
        if correct_b3 == :
            return result
        else:
            print("DATA END ERROER")



            


