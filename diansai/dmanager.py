import pickle
import numpy as np
import scipy.io as io


class DataManager:
    def __init__(self, sample_size=2, max_sample=50):
        self.sample_size = sample_size
        self.make_sample = max_sample
        try:
            with open("/home/pi/diansai/data_for_train.p", "rb") as f:
                self.data_set = pickle.load(f)
        except FileNotFoundError:
            with open("/home/pi/diansai/data_for_train.p", "wb") as f:
                self.data_set = [[[0], -1]]
                pickle.dump(self.data_set, f)
        self.index = self.make_index()
        self.latest_number = []
        self.latest_number_quantity = self.get_number_to_record()

    def make_index(self):
        index = [i[1] for i in self.data_set]
        res = {}
        for i in index:
            res[i] = res.get(i, 0) + 1
        return res

    def get_number_to_record(self):
        self.index = self.make_index()
        self.latest_number = max([k for k in self.index.keys()])
        if self.latest_number == -1:
            self.latest_number += 1
            self.latest_number_quantity = 0
            return int(self.latest_number)
        if self.latest_number > self.make_sample:
            self.latest_number = 0
            self.latest_number_quantity = 0
            return self.latest_number
        self.latest_number_quantity = self.index[self.latest_number]
        if self.latest_number_quantity >= self.sample_size:
            self.latest_number_quantity = 0
            self.latest_number += 1
        return int(self.latest_number)

    def record_data(self, data, label):
        sample = [data, label]
        self.data_set.append(sample)
        with open("/home/pi/diansai/data_for_train.p", "wb") as f:
            pickle.dump(self.data_set, f)

    def convert_to_mat(self):
        data = self.data_set[1:]
        X, Y = np.array([i[0] for i in data]), np.array([i[1] for i in data])
        data_matlab = {}
        data_matlab["X"], data_matlab['Y'] = X, Y
        io.savemat("data_for_train.mat", data_matlab)


if __name__ == '__main__':
    data_manager = DataManager()
    data_manager.record_data([1, 323, 3, 3434, 34324, 234234], 1)
    print(data_manager.make_index())
