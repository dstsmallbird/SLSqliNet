from gc import callbacks
import os
from tabnanny import verbose

# configure gpu device
gpu_index = 6
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICE']=str(gpu_index)
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"



import sys
import time
import numpy as np
import tensorflow as tf
from loguru import logger
from datetime import datetime
from keras.models import Sequential
from keras.layers import LSTM, Bidirectional, Dense
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.utils import class_weight

sys.path.append("../")
from utils.data import data
from utils.config import config
from utils.evaluate import evaluate_sklearn
from utils.evaluate import write_evaluation_result
from utils.evaluate import plot_loss_acc
from utils.evaluate import save_history


# create LSTM model and train it
@logger.catch
def train_bilstm(app, vect, gpu_index):
    # epoch_bilstm = config["model"]["epoch_bilstm"]
    # batch_size_bilstm = config["model"]["batch_size_bilstm"]
    epoch_bilstm = 150
    batch_size_bilstm = 128

    # load train set, test set and validation set based on the proportion -- 6:3:1
    d_instance = data(app, gpu_index)
    if vect == 'int':
        train_data, test_data, val_data, train_label, test_label, val_label = d_instance.get_train_test_val_set()
    else:
        train_data, test_data, val_data, train_label, test_label, val_label = d_instance.get_tf_albert_dataset(True, batch_size_bilstm)
    
    # define and compile model
    model = Sequential()
    model.add(Bidirectional(
        LSTM(128, dropout=0.2, recurrent_dropout=0.2),
        input_shape = (1, 768)
    ))
    model.add(Dense(6, activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()

    # Train
    logger.debug("Training ... epoch: {}, batch_size: {}", epoch_bilstm, batch_size_bilstm)
    # 调整学习率
    factor = 0.5
    # reduce_lr = ReduceLROnPlateau(monitor='val_loss', patience=10, mode='auto', verbose=1)
    # reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=factor, patience=5, min_lr=0.001)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=factor, patience=5, min_delta=0.0001, min_lr=0, verbose=1)
    logger.info("[Learning Rate Factor] {}", factor)
    start_time = datetime.now()
    history = model.fit(
        train_data,
        train_label,
        epochs = epoch_bilstm,
        batch_size = batch_size_bilstm,
        validation_data = (val_data, val_label),
        # callbacks=[EarlyStopping(monitor='val_loss', patience=3, min_delta=0.0001)],
        callbacks = [reduce_lr],
        verbose=2
    )
    end_time = datetime.now()
    time_diff = end_time - start_time                                           # 时间差
    milliseconds = time_diff.seconds * 1000 + time_diff.microseconds / 1000     # 毫秒级时间差
    logger.info("Train time: {} ms, {} s, {} min", milliseconds, time_diff.seconds, time_diff.seconds / 60)

    # paint loss/accuracy curve and save the train history
    time_stamp = time.strftime("%y%m%d-%H%M",time.localtime())
    loss_fig_name = "{}_{}_{}_loss.png".format(time_stamp, app, vect)
    acc_fig_name = "{}_{}_{}_acc.png".format(time_stamp, app, vect)
    plot_loss_acc(history.history, "loss", loss_fig_name)
    plot_loss_acc(history.history, "accuracy", acc_fig_name)
    save_history(history.history, "BiLSTM", app, vect)

    # save model
    model_name = "{}_{}_bilstm.model".format(app, vect)
    model.save(model_name)

    # Predict
    logger.debug("Predicting ...")
    start_time = datetime.now()
    predict_prop = model.predict(test_data)
    predict_label = np.argmax(predict_prop, axis=1)
    end_time = datetime.now()
    time_diff = end_time - start_time                                           # 时间差
    milliseconds = time_diff.seconds * 1000 + time_diff.microseconds / 1000     # 毫秒级时间差
    logger.info("Predict time: {} ms, {} s, {} min", milliseconds, time_diff.seconds, time_diff.seconds / 60)

    # evaluate the predict result
    logger.debug("Evaluating ...")
    fig_name = "{}_{}_bilstm_confusion_matrix.png".format(app, vect)
    metric_sklearn = evaluate_sklearn(predict_label, test_label, fig_name)

    # write the evaluation result into file
    write_evaluation_result('BiLSTM', app, vect, metric_sklearn)


def get_cw(app, gpu_index):
    d_instance = data(app, gpu_index)
    train_data, test_data, val_data, train_label, test_label, val_label = d_instance.get_tf_albert_dataset(True, 256)
    # class_weights = dict(zip(np.unique(train_label.numpy()), class_weight.compute_class_weight('balanced', np.unique(train_label.numpy()), train_label.numpy())))
    class_weights = class_weight.compute_class_weight('balanced', np.unique(train_label.numpy()), train_label.numpy())
    print(class_weights)

if __name__ == "__main__":
    logger.add("bilstm.log")

    # "web_app" or "wordpress"
    app = "wordpress"
    # "albert" or "int"
    vect = "albert"
    
    # set gpu device
    logger.debug("phisical gpu: {}", tf.config.experimental.list_physical_devices('GPU'))
    gpus = tf.config.experimental.list_physical_devices('GPU')
    tf.config.experimental.set_visible_devices(gpus[gpu_index], 'GPU')
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    logger.debug("logical gpu: {}", logical_gpus)
    
    train_bilstm(app, vect, gpu_index)

    # get_cw("web_app", gpu_index)
