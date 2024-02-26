from pandas import read_csv
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import hist, plot


X_data = read_csv("data_three.csv", header=None).values
raw = [[i, i, i] for i in range(0, 51)]
Y_data = []
for i in raw:
    Y_data += i


def show_random_samples(X, Y):
    y_set = set(Y)
    n_class = len(y_set)
    labels = []
    Y = np.array(Y)
    fig, ax = plt.subplots()
    for class_idx in range(1, n_class):
        cur_X = X[Y == class_idx]
        cur_data = cur_X[np.random.randint(cur_X.shape[0], size=1)][0]
        time = np.linspace(0, 2, cur_X.shape[1]-2)
        ax.plot(time, cur_data[:-2])
        labels.append(class_idx)
    plt.legend(labels)
    plt.xlabel("time")
    plt.ylabel("C")
    plt.title('Random Samples from Different Classes')
    plt.show()


def show_sample_var(X, Y):
    y_set = set(Y)
    n_class = len(y_set)
    labels, sum_of_var = [], []
    Y = np.array(Y)
    fig, ax = plt.subplots()
    numbers = []

    for class_idx in range(1, n_class):
        cur_X = X[Y == class_idx]
        delta_1_2 = np.mean(cur_X[0, :] - cur_X[1, :])
        delta_2_3 = np.mean(cur_X[1, :] - cur_X[2, :])
        delta_3_1 = np.mean(cur_X[0, :] - cur_X[2, :])
        numbers.append(delta_1_2)
        numbers.append(delta_2_3)
        numbers.append(delta_3_1)
    counts, bins, _ = ax.hist(numbers, 100, normed=True)
    ax2 = ax.twinx()
    cum = np.cumsum(counts) / np.sum(counts)
    ax2.plot(bins[1:], cum, c="red")

    plt.xlabel("var")
    plt.ylabel("C")
    plt.title('Distribution of Delta between Different Temperature')
    plt.show()

L, C = 6, 6

f_sen = X_data[:, :-2]
c_sen = 1 / L * (2*np.pi * f_sen) - C
print(c_sen)

# 首先观察随机的样本
show_random_samples(X_data, Y_data)
# 然后查看一下差值们的分布，不同温度下的差值大部分都分布在0附近
# 该图可见，不同温度间的差值趋向于0
show_sample_var(X_data, Y_data)

