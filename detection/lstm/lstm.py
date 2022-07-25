import os

# configure gpu device
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICE']='7'

os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"

# from keras import backend as K
#import tensorflow as tf
#from keras.backend import set_session

# set GPU memory 
# if('tensorflow' == K.backend()):
# import tensorflow as tf
# from keras.backend import set_session
# config = tf.compat.v1.ConfigProto()
# config.gpu_options.visible_device_list = '7'
# # config.gpu_options.allow_growth = True
# config.gpu_options.per_process_gpu_memory_fraction = 0.85
# set_session(tf.compat.v1.Session(config=config))


import sys
import time
import pynvml
import numpy as np
import tensorflow as tf
from loguru import logger
from datetime import datetime
from keras.models import Sequential
from keras.layers import LSTM, Activation, Dense
from keras.callbacks import EarlyStopping

sys.path.append("../")
from utils.data import data
from utils.config import config
from utils.evaluate import evaluate_sklearn
from utils.evaluate import write_evaluation_result
from utils.evaluate import plot_loss_acc
from utils.evaluate import save_history


# create LSTM model and train it
@logger.catch
def train_lstm(app, vect):
    epoch_lstm = config["model"]["epoch_lstm"]
    batch_size_lstm = config["model"]["batch_size_lstm"]

    # load train set, test set and validation set based on the proportion -- 6:3:1
    d_instance = data(app)
    if vect == 'int':
        train_data, test_data, val_data, train_label, test_label, val_label = d_instance.get_train_test_val_set()
    else:
        train_data, test_data, val_data, train_label, test_label, val_label = d_instance.get_tf_albert_dataset(True, batch_size_lstm)       
    
    # define and compile model
    model = Sequential()
    model.add(LSTM(128, input_shape = (1, 768), dropout=0.2, recurrent_dropout=0.2))     # 128 hidden cells
    model.add(Dense(6, activation='softmax'))                                                   # output layer: 6 categories
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # GPU id is 7
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(7)
    meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
    logger.debug("Memory used: {} G, free: {} G, {} M", meminfo.used / 1024 ** 3, meminfo.free / 1024 ** 3, meminfo.free / 1024 ** 2)
    model.summary()

    # Train
    logger.debug("Training ... epoch: {}, batch_size: {}", epoch_lstm, batch_size_lstm)
    start_time = datetime.now()
    history = model.fit(
        train_data,
        train_label,
        epochs = epoch_lstm,
        batch_size = batch_size_lstm,
        validation_data = (val_data, val_label),
        # callbacks=[EarlyStopping(monitor='val_loss', patience=3, min_delta=0.0001)],
        verbose=2
    )
    end_time = datetime.now()
    logger.info("Train time: {} s, {} min", (end_time - start_time).seconds, (end_time - start_time).seconds / 60)

    # paint loss/accuracy curve and save the train history
    time_stamp = time.strftime("%y%m%d-%H%M",time.localtime())
    loss_fig_name = "{}_{}_{}_loss.png".format(time_stamp, app, vect)
    acc_fig_name = "{}_{}_{}_acc.png".format(time_stamp, app, vect)
    plot_loss_acc(history.history, "loss", loss_fig_name)
    plot_loss_acc(history.history, "accuracy", acc_fig_name)
    save_history(history.history, "LSTM", app, vect)

    # save model
    model_name = "{}_{}_lstm.model".format(app, vect)
    model.save(model_name)

    # Predict
    logger.debug("Predicting ...")
    start_time = datetime.now()
    predict_prop = model.predict(test_data)
    predict_label = np.argmax(predict_prop, axis=1)
    end_time = datetime.now()
    logger.info("Predict time: {} s, {} min", (end_time - start_time).seconds, (end_time - start_time).seconds / 60)

    # evaluate the predict result
    logger.debug("Evaluating ...")
    fig_name = "{}_{}_lstm_confusion_matrix.png".format(app, vect)
    metric_sklearn = evaluate_sklearn(predict_label, test_label, fig_name)

    # write the evaluation result into file
    write_evaluation_result('LSTM', app, vect, metric_sklearn)


if __name__ == "__main__":
    logger.add("lstm.log")

    # "web_app" or "wordpress"
    app = "wordpress"
    # "albert" or "int"
    vect = "albert"
    
    # set gpu device (gpu:7)
    logger.debug("phisical gpu: {}", tf.config.experimental.list_physical_devices('GPU'))
    gpus = tf.config.experimental.list_physical_devices('GPU')
    tf.config.experimental.set_visible_devices(gpus[7], 'GPU')
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    logger.debug("logical gpu: {}", logical_gpus)
    
    train_lstm(app, vect)
