import serial
import os


class Sensor:
    def __init__(self):
        dev_path = self.find_tty_usb()
        if dev_path is None:
            print("FAILED!")
        else:            
            self.ser = serial.Serial(dev_path, 115200)
            print("CONNECTED!")

    def find_tty_usb(self, root_dir="/dev", ext=None):
        head = 'ttyUSB'
        names_list = []
        paths_list = []
        for parent, _, fileNames in os.walk(root_dir):
            for name in fileNames:
                if name.startswith('.'):
                    continue
                if ext:
                    if name.endswith(tuple(ext)):
                        names_list.append(name)
                        paths_list.append(os.path.join(parent, name))
                else:
                    names_list.append(name)
                    paths_list.append(os.path.join(parent, name))
        _name_list = [name[:-1] for name in names_list]
        if head in _name_list:
            return paths_list[_name_list.index(head)]
        else:
            print("ttyUSB PORT NOT FOUND!")
            return None

    def send_result(self, data):
        self.ser.write(b'\xAA')
        self.ser.write(b'\xAA')
        for i in range(3):
            self.ser.write(data)
        self.ser.write(b'\n')

    def send_requirement(self, data):
        self.ser.write(b'\xBB')
        self.ser.write(b'\xBB')
        for i in range(3):
            self.ser.write(data)
        self.ser.write(b'\n')

    def get_data(self):
        if self.ser.in_waiting == 0:
            return None
        else:
            data = self.ser.readline()
        return data


if __name__ == '__main__':
    sensor = Sensor()
    print(sensor.get_data())
