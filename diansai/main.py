# coding:utf-8
from readfdc import Sensor
# from three_layer_ann import ThreeLayerAnn
from dmanager import DataManager
import random

class User:
    def __init__(self):
        self.port = Sensor()
        self.mode = 'MEASURE'
        self.data_manager = DataManager()
        self.label = None
        self.tempurature_and_humidty = 0, 0
        # self.model = ThreeLayerAnn(with_weighted=False)
        self.port.send_result(99)

    def run(self):
        while True:
            cmd_and_data = self.port.get_data()
            if cmd_and_data is None:
                continue
            else:
                cmd_and_data = str(cmd_and_data)

            # print(cmd_and_data)

            if len(cmd_and_data) > 3:
                cmd, data = cmd_and_data.split(",")[0], cmd_and_data.split(",")[1:-1]
            else:
                cmd, data = cmd_and_data.split(",")[0], None
                self.mode = "CORRECTION"

            # run commands
            if str(cmd) == "b'\\xaa\\xaa":
                # measure
                print('get measure data')
                self.mode = "MEASURE"
                self.label = None
                data = data + self.tempurature_and_humidty
                print("get data :", data)
                # result = self.model.predict(data)
                result = random.randrange(0, 51)
                self.port.send_result(result)
                print("send result: ", result)

            elif str(cmd) == "b'\\xbb\\xbb":
                # correction
                print("CORRECTION!")
                self.mode = "CORRECTION"
                if self.label is None:
                    self.label = self.data_manager.get_number_to_record()
                    self.port.send_requirement(self.label)
                else:
                    print("RECORD DATA AS", self.label)
                    data = [int(d) for d in data] + self.tempurature_and_humidty
                    self.data_manager.record_data(data, label=self.label)
                    print(data)
                    self.label = self.data_manager.get_number_to_record()
                    self.port.send_requirement(self.label)

            elif str(cmd) == "b'\\xcc\\xcc":
                """
                get tempurature and humidty
                """
                self.tempurature_and_humidty = [int(data[0]) + float(data[1]) / 10,
                                                int(data[2]) + float(data[3]) / 10]
                print("Get Tempurature and Humidty", self.tempurature_and_humidty)


if __name__ == '__main__':
    user = User()
    user.run()
