from readfdc import Sensor
from three_layer_ann import ThreeLayerAnn
from dmanager import DataManager


class User:
    def __init__(self):
        self.port = Sensor()
        self.mode = 'MEASURE'
        self.data_manager = DataManager()
        self.label = None
        self.model = ThreeLayerAnn(with_weighted=False)

    def run(self):
        while True:
            cmd_and_data = self.port.get_data()
            if cmd_and_data is None:
                continue

            if len(cmd_and_data) > 3:
                cmd, data = cmd_and_data.split(",")[0], cmd_and_data.split(",")[1:-1]
            else:
                cmd, data = cmd_and_data.split(",")[0], None
                self.mode = "CORRECTION"

            if cmd == "\xAA\xAA":
                # measure
                self.mode = "MEASURE"
                result = self.model.predict(data)
                self.port.send_result(result)

            elif cmd == "\xBB\xBB":
                # correction
                self.mode = "CORRECTION"
                if self.label is None:
                    self.label = self.data_manager.get_number_to_record()
                    self.port.send_requirement(self.label)
                else:
                    self.data_manager.record_data(data, label=self.label)






