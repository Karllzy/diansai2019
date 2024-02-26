from keras import Input, Model
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.models import load_model
from keras.layers import Dense
from scipy.io import loadmat
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import datetime
import itertools
import numpy as np


class ThreeLayerAnn:
    """
    使用3层神经网络拟合可能的输入输出关系
    为了增加拟合成功的可靠性，增加数据的维度:
    输入数据：
        x, log(x)
    """

    def __init__(self, with_weighted=False):
        self.layer_sizes = [2, 5, 1]
        self.layer_activations = ["sigmoid", "sigmoid", "relu"]
        self.learning_rate, self.num_epoches, self.batch_size = 1e-5, 50000, 600
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

    def make_confusion_matrix(self, x, y_true, normalize=True, save_as_name=None):
        y_pred = self.predict(x).astype(int)
        cm = confusion_matrix(y_true, y_pred)
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            if save_as_name is not None:
                save_as_name += "_normalized"

        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title('Confusion Matrix')
        plt.colorbar()

        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.tight_layout()
        if save_as_name is not None:
            plt.savefig(save_as_name + "_confusion_matrix.tif", dpi=600)
        plt.show()
        return cm


if __name__ == '__main__':
    from preprocess import get_data_and_process

    train_x, train_y = get_data_and_process("/home/zhenye/桌面/diansai_nor/A_group")
    print("data shape: x : ", train_x.shape, 'y : ', train_y.shape)
    # 固定随机数
    random_seed = 12
    # 是否使用已经训练好的权重
    if_with_weighted = False

    np.random.seed(random_seed)

    X_train, X_test, Y_train, Y_test = train_test_split(train_x, train_y, test_size=0.3, random_state=random_seed)
    name, class_names = "three_layer_ann", [i for i in range(1, 51)]

    if if_with_weighted:
        ann = ThreeLayerAnn(with_weighted=True)
        ann.train(X=X_train, Y=Y_train, validation_x=X_test, validation_y=Y_test)
    else:
        ann = ThreeLayerAnn()
        ann.train(X=X_train, Y=Y_train, validation_x=X_test, validation_y=Y_test)

    # 保存迷惑矩阵，上面一行可以进行标准化
    ann.make_confusion_matrix(x=train_x, y_true=train_y, save_as_name=name, normalize=True)
    # ann.make_confusion_matrix(x=train_x, y_true=train_y, save_as_name=name, normalize=False)

