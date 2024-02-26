import pickle
import matplotlib.pyplot as plt
import numpy as np
import os


def most_mean(data, accuracy=10):
    count, bins_range = np.histogram(data, bins=accuracy)
    most_range_index = np.argmax(count)
    left_boud, right_boud = bins_range[most_range_index], bins_range[most_range_index+1]
    data_for_mean = data[data <= right_boud]
    data_for_mean = data_for_mean[data_for_mean >= left_boud]
    most_mean = np.mean(data_for_mean)
    return most_mean


def read_data(data_file_name):
    with open(data_file_name, "rb") as f:
        data_set = pickle.load(f)
    data_set = data_set[1:]
    data, Y = [d[0] for d in data_set], [d[1] for d in data_set]
    data, Y = np.array(data), np.array(Y)
    return data, Y


def data_preprocess(X):
    print(X)
    data = X[:, :-2]  # drop T
    data = data[2:, :]  # drop 0

    data = [most_mean(d) for d in data]
    x1 = np.array(data)
    x2 = np.log(data)
    X = np.vstack([x1, x2])
    return X.T


def listdir_files(root_dir, ext=None):
    """
    列出文件夹中的文件
    :param root_dir: 根目录
    :param ext: 类型
    :return: [文件路径(相对路径), 文件夹名称, 文件名称]
    """
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
    return paths_list, names_list


def get_data_and_process(path):
    path_list, _ = listdir_files(path, ext="p")
    correciton_list = [10, 20, 30, 40]

    data_X, data_Y = [], []
    for data_file in path_list:
        X, Y = read_data(data_file)
        Y = Y[2:]
        X = data_preprocess(X)
        data_Y.append(Y)
        data_X.append(X)
    data_X = np.vstack(data_X)
    data_Y = np.hstack(data_Y)

    correction_std = []
    for correc_level in correciton_list:
        data_to_mean = data_X[data_Y == correc_level]
        strand_mean = np.mean(data_to_mean, axis=1)
        print(strand_mean)
        correction_std.append(strand_mean[0])
    with open("correction_std.p", "wb") as f:
        pickle.dump(correction_std, f)
    print(correction_std)

    max_x, min_x = np.max(data_X, axis=0), np.min(data_X, axis=0)
    dist = max_x - min_x

    # Normalize with open
    with open("max_min_dist.p", "wb") as f:
        pickle.dump([max_x, min_x, dist], f)
    data_X = np.array([(one_row - min_x) / dist for one_row in data_X])

    return data_X, data_Y


def show_wave_pic(path, if_with_0=False, single_data=None, color_list=None):
    with open(path, "rb") as f:
        data_set = pickle.load(f)

    data_set = data_set[1:]  # 去除数据头
    data = np.array([d[0] for d in data_set])
    if if_with_0:
        data = data[:, :-2]
    else:
        data = data[2:, :-2]

    time = np.linspace(0, 3, 500)

    if single_data is not None and color_list is not None:

        for select_num, color in zip(single_data, color_list):
            plt.plot(time, data[select_num:select_num + 2, :].T, c=color)
            raw_data = data[select_num, :]
            mean_data = most_mean(raw_data)
            print(mean_data)

        plt.ylabel('F_sensor')
        plt.xlabel('Time')
        plt.title('Wave of F_sensor')
        plt.show()
    else:
        plt.plot(time, data.T)
        plt.ylabel('F_sensor')
        plt.xlabel('Time')
        plt.title('Wave of F_sensor')
        plt.show()


if __name__ == '__main__':

    show_wave_pic("/home/zhenye/桌面/diansai_nor/B_group/7a614.p",
                  if_with_0=False,
                  single_data=[1, 2, 3, 4, 5],
                  color_list=["red", "green", "blue", "black", "purple"])
    # X, Y = read_data("/home/zhenye/桌面/测试数据/1.p")
    #
    # # 绘制多曲线图
    # print(X[:, :-2].shape)
    # x = X[:, :-2]
    # time = np.linspace(0, 2, 200)
    # # plt.plot(time, x.T)
    # # plt.show()
    #
    # # 绘制most mean
    # num = 6
    # print(x[num, :].shape)
    # most_mean_plot = most_mean(x[num, :]) * (np.zeros(200) + 1)
    # plt.plot(time, most_mean_plot)
    # plt.plot(time, x[num, :])
    # plt.show()
    # # num = 92
    # # most_mean_plot = most_mean(x[num, :]) * (np.zeros(200) + 1)
    # # plt.plot(time, most_mean_plot)
    # # plt.plot(time, x[num, :])
    # # num = 94
    # # most_mean_plot = most_mean(x[num, :]) * (np.zeros(200) + 1)
    # # plt.plot(time, most_mean_plot)
    # # plt.plot(time, x[num, :])
    # # num = 96
    # # most_mean_plot = most_mean(x[num, :]) * (np.zeros(200) + 1)
    # # plt.plot(time, most_mean_plot)
    # # plt.plot(time, x[num, :])
    # # plt.show()
    #
    # train_x, train_y = get_data_and_process("/home/zhenye/桌面/测试数据/")
    # print(train_x.shape, train_y.shape)
    # import scipy.io as io
    # data_for_matlab = {}
    # data_for_matlab["X"], data_for_matlab["Y"] = train_x, train_y
    # io.savemat("data_for_matlab.mat", data_for_matlab)

