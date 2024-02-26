# coding:utf-8
from keras import Input, Model
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.models import load_model
from keras.layers import Dense
from scipy.io import loadmat
# from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import datetime
import itertools
import numpy as np


class ThreeLayerAnn:
    """
    使用3层神经网络拟合可能的输入输出关系
    为了增加拟合成功的可靠性，增加数据的维度:
    输入数据：
        校验值常量c, x, x^2, x^3, x^4
    """

    def __init__(self, with_weighted=False):
        self.layer_sizes = [5, 18, 50]
        self.layer_activations = ["relu", "relu", "softmax"]
        self.learning_rate, self.num_epoches, self.batch_size = 1e-3, 5, 2000
        if with_weighted is False:
            self.model = self.build_model()
        else:
            self.model = load_model("three_layers_ann_latest_weights.hdf5")

    def build_model(self):
        input_layer = Input(shape=(self.layer_sizes[0], ), name="input_layer")
        x = Dense(self.layer_sizes[0], name="Dense1", activation=self.layer_activations[0])(input_layer)
        x = Dense(self.layer_sizes[1], name='Dense2', activation=self.layer_activations[1])(x)
        output = Dense(self.layer_sizes[2], name="Output", activation=self.layer_activations[2])(x)

        model = Model(inputs=input_layer, outputs=output)
        model.compile(loss='mse', optimizer='Adam', metrics=['accuracy'])
        print(model.summary())
        print("Build Model Success!!")
        return model

    def train(self, X, Y, validation_x, validation_y):
        callbacks, file_path = [], "three_layers_ann_latest_weights.hdf5"
        checkpoint = ModelCheckpoint(filepath=file_path, monitor="val_acc", mode="max", save_best_only=True)
        early_stop = EarlyStopping(monitor='val_loss', min_delta=0, patience=100000, verbose=0, mode='auto')
        callbacks.append(checkpoint)
        callbacks.append(early_stop)
        history = self.model.fit(X, Y, epochs=self.num_epoches, verbose=2, batch_size=self.batch_size,
                                 validation_data=(validation_x, validation_y), callbacks=callbacks)
        return history

    def predict(self, x):
        return self.model.predict(x)

    # def make_confusion_matrix(self, x, y_true, class_names, normalize=True, save_as_name=None):
    #     y_pred = np.argmax(self.predict(x), axis=1)
    #     print(y_pred.shape)
    #     y_true = np.argmax(y_true, axis=1)
    #     print(y_true)
    #     cm = confusion_matrix(y_true, y_pred)
    #     if normalize:
    #         cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    #         if save_as_name is not None:
    #             save_as_name += "_normalized"
    #
    #     plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    #     plt.title('Confusion Matrix')
    #     plt.colorbar()
    #     tick_marks = np.arange(len(class_names))
    #     plt.xticks(tick_marks, class_names, rotation=45)
    #     plt.yticks(tick_marks, class_names)
    #
    #     fmt = '.2f' if normalize else 'd'
    #     thresh = cm.max() / 2.
    #     for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    #         plt.text(j, i, format(cm[i, j], fmt),
    #                  horizontalalignment="center",
    #                  color="white" if cm[i, j] > thresh else "black")
    #     plt.ylabel('True label')
    #     plt.xlabel('Predicted label')
    #     plt.tight_layout()
    #     if save_as_name is not None:
    #         plt.savefig(save_as_name + "_confusion_matrix.tif", dpi=600)
    #     plt.show()
    #     return cm


# def load_data_set():
#     data = loadmat("class_data_2019-06-23_09_13_18.mat")
#     # 前百分之30为测试集
#     _num = int(data['0'].shape[0] * 0.3)
#     data_1 = np.repeat(np.array([1, 0, 0, 0]), _num, axis=0)
#     data_2 = np.repeat(np.array([0, 1, 0, 0]), _num, axis=0)
#     data_3 = np.repeat(np.array([0, 0, 1, 0]), _num, axis=0)
#     data_4 = np.repeat(np.array([0, 0, 0, 1]), _num, axis=0)
#
#     test_y = np.vstack((data_1, data_2, data_3, data_4)).T
#     test_x = np.vstack((data["0"][:_num], data["1"][:_num], data["2"][:_num], data["3"][:_num]))
#
#     # 后70%为训练集
#     _num = int(data['0'].shape[0] * 0.7)
#     data_1 = np.repeat(np.array([1, 0, 0, 0]), _num, axis=0)
#     data_2 = np.repeat(np.array([0, 1, 0, 0]), _num, axis=0)
#     data_3 = np.repeat(np.array([0, 0, 1, 0]), _num, axis=0)
#     data_4 = np.repeat(np.array([0, 0, 0, 1]), _num, axis=0)
#
#     train_y = np.vstack((data_1, data_2, data_3, data_4)).T
#     train_x = np.vstack((data["0"][-_num:], data["1"][-_num:], data["2"][-_num:], data["3"][-_num:]))
#     split_point = train_x.shape[1]
#     train_data = np.hstack((train_x, train_y))
#     np.random.shuffle(train_data)
#     train_x, train_y = train_data[:, :split_point], train_data[:, split_point:]
#     return train_x, test_x, train_y, test_y


if __name__ == '__main__':
    # 固定随机数
    np.random.seed(12)
    # 是否使用已经训练好的权重
    if_with_weighted = False

    # train_X, test_X, train_Y, test_Y = load_data_set()
    # name, class_names = "three_layer_ann", [i for i in range(0, 10)]

    if if_with_weighted:
        ann = ThreeLayerAnn(with_weighted=True)
    else:
        ann = ThreeLayerAnn()
        # X_train, X_test, Y_train, Y_test = train_test_split(train_X, train_Y, test_size=0.3)
        # ann.train(X=X_train, Y=Y_train, validation_x=X_test, validation_y=Y_test)

    # 保存迷惑矩阵，上面一行可以进行标准化
    # ann.make_confusion_matrix(x=test_x, y_true=test_y, class_names=class_names, save_as_name=name, normalize=True)
    # ann.make_confusion_matrix(x=test_X, y_true=test_Y, class_names=class_names, save_as_name=name, normalize=False)
