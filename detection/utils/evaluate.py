import json
import numpy as np
import time
from loguru import logger
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from .config import config


@logger.catch
def evaluate_sklearn(predict_label, actual_label, fig_name):
    # if len(set(actual_label)) == 2:
    #     target_names = ["normal", "abnormal"]
    # else:
    #     target_names = ["time blind", "bool blind", "illegal", "tautology", "union", "normal"]
    
    target_names = ["time blind", "bool blind", "illegal", "tautology", "union", "normal"]
    
    metric_str = classification_report(actual_label, predict_label, target_names=target_names)
    metric_dict = classification_report(actual_label, predict_label, target_names=target_names, output_dict=True)
    logger.info("[Metric]\n{}", metric_str)
    logger.info("[Accuracy] {}", metric_dict["accuracy"])

    # calculate the confusion matrix
    confusion = confusion_matrix(actual_label, predict_label)
    logger.info("Confusion Matrix\n{}", confusion)

    # paint
    plot_confusion_matrix(confusion, fig_name)

    metric_cm = {
        "Various metric": metric_dict,
        "Confusion matrix": confusion.tolist()
    }

    return metric_cm


@logger.catch
def binary_classification(log_file, cm_file, fig_name):
    logger.add(log_file)

    # load confusion matrix from file
    with open(cm_file, "r") as f_read:
        metric_cm = json.load(f_read)
    cm = np.array(metric_cm["Confusion matrix"], dtype=np.int16)  # confusion matrix
    
    sum_row = np.sum(cm, axis=1)                        # sum of row: actual label count
    sum_col = np.sum(cm, axis=0)                        # sum of column: predict lable count
    actual_abnormal = np.sum(sum_row) - sum_row[-1]     # actual label count of abnormal: "time blind", "bool blind", "illegal", "tautology", "union"
    actual_normal = sum_row[-1]                         # actual label count of normal: "normal"
    predict_abnormal = np.sum(sum_col) - sum_col[-1]    # predict label count of abnormal: "time blind", "bool blind", "illegal", "tautology", "union"
    predict_normal = sum_col[-1]                        # predict label count of normal: "normal"
    
    TP = actual_abnormal
    FP = 0
    FN = 0
    TN = cm[-1][-1]
    for i in range(5):
        TP -= cm[i][-1]
        FN += cm[i][-1]
        FP += cm[-1][i]

    acc1 = (TP + TN) / (actual_abnormal + actual_normal)
    acc2 = (TP + TN) / (TP + TN + FP + FN)

    precision1 = TP / (TP + FP)
    precision2 = TP / predict_abnormal

    recall1 = TP / (TP + FN)
    recall2 = TP / actual_abnormal

    F11 = (2 * precision1 * recall1) / (precision1 + recall1)
    F12 = (2 * precision2 * recall2) / (precision2 + recall2)

    FPR = FP / (FP + TN)    # false positive rate
    FNR = FN / (FN + TP)    # false negative rate

    binary_cm = np.array([[TN, FP], [FN, TP]])
    logger.info("Confusion matrix:\n{}", binary_cm)
    logger.info("[Actual] normal: {}, abnormal: {}", actual_normal, actual_abnormal)
    logger.info("[Predict] normal: {}, abnormal: {}", predict_normal, predict_abnormal)
    logger.info(
        "[Metric] accuracy: {:.2%}, precision: {:.2%}, recall: {:.2%}, F1-score: {:.2%}, FPR: {:.2%}, FNR: {:.2%}",
        acc1,
        precision1,
        recall1,
        F11,
        FPR,
        FNR
    )
    plot_confusion_matrix(binary_cm, fig_name)


@logger.catch
def plot_confusion_matrix(confusion, fig_name):
    plt.clf()   # clear previous figure
    if len(confusion) == 2:
        classes_name = ["normal", "abnormal"]
    else:
        classes_name = ["time blind", "bool blind", "illegal", "tautology", "union", "normal"]
    indices = range(len(confusion))
    thresh = confusion.max() / 2

    # 绘制热度图
    plt.imshow(confusion, cmap=plt.cm.Blues)
    if len(confusion) == 2:
        plt.xticks(indices, classes_name)
    else:
        plt.xticks(indices, classes_name, rotation=-15)
    plt.yticks(indices, classes_name)
    plt.colorbar()
    plt.xlabel('Predict label')
    plt.ylabel('Actual label')
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.15)

    # 显示数据
    for first_index in range(len(confusion)):   # row
        for second_index in range(len(confusion[first_index])): # column
            plt.text(
                second_index, 
                first_index, 
                confusion[first_index][second_index], color="white" if confusion[first_index, second_index] > thresh else "black", 
                horizontalalignment="center"
            )

    # save picture
    logger.info("Figure of current confusion-matric: {}", fig_name)
    plt.savefig(fig_name, format='png')


@logger.catch
def write_evaluation_result(model_name, app, vect, evaluation_result):
    output_path = config["env"]["output_path"]
    time_stamp = time.strftime("%y%m%d-%H%M",time.localtime())
    output_file = "{}{}_{}_{}_{}_evaluation.json".format(output_path, time_stamp, app, vect, model_name)
    
    # write the evaluation result into file
    logger.debug("Output evaluation result to file: {}", output_file)
    with open(output_file, 'w') as f:
        f.write(json.dumps(evaluation_result))


@logger.catch
def plot_loss_acc(data, type_str, fig_name):
    plt.clf()   # clear previous figure
    y_label = "Loss" if type_str == "loss" else "Accuracy"
    
    # plot loss curve
    plt.plot(data[type_str])
    plt.plot(data["val_" + type_str])
    plt.xlabel("Epochs")
    plt.ylabel(y_label)
    plt.legend(["Train " + y_label, 'Validation ' + y_label])

    # save curve
    logger.debug("Save {} curve: {}", type_str, fig_name)
    logger.info("[Train {}]: {}", y_label, data[type_str])
    logger.info("[validation {}]: {}", y_label, data["val_" + type_str])
    plt.savefig(fig_name, format='png')


@logger.catch
def save_history(history, model_name, app, vect):
    output_path = config["env"]["output_path"]
    time_stamp = time.strftime("%y%m%d-%H%M",time.localtime())
    output_file = "{}{}_{}_{}_{}_history.json".format(output_path, time_stamp, app, vect, model_name, )
    
    # write the train history into file
    logger.debug("Output train history to file: {}", output_file)
    with open(output_file, 'w') as f:
        f.write(json.dumps(str(history)))
