import numpy as np
import sys
from datetime import datetime
import time
from sklearn import svm
from sklearn.model_selection import GridSearchCV
import joblib
from loguru import logger

sys.path.append("../")
from utils.data import data
from utils.evaluate import evaluate_sklearn
from utils.evaluate import write_evaluation_result


# save predict label
def save_label(predict_label, filename):
    '''
    save predic label to file by using numpy.tofile function
    param:
        predict_label: predict labels of SVM model
        filename: the file name of saving predict label
    '''
    logger.info("Save predict label to file: {}", filename)
    predict_label = np.array(predict_label, dtype=np.int8)
    predict_label.tofile(filename)


# train svm without grid search
def train_svm(app, vect):
    # load all samples and divide them into train set, test set and validation set based on the proportion -- 6:3:1
    d_instance = data(app, -1)
    if vect == 'int':
        train_data, test_data, val_data, train_label, test_label, val_label = d_instance.get_train_test_val_set()
    else:
        train_data, test_data, val_data, train_label, test_label, val_label = d_instance.get_word_embedding_train_test_val_set()

    # train    
    clf = svm.SVC(decision_function_shape='ovr', class_weight="balanced")
    logger.debug("Start training ...")
    start_time = datetime.now()
    clf.fit(train_data, train_label)
    end_time = datetime.now()
    time_diff = end_time - start_time                                            # 时间差
    milliseconds = time_diff.seconds * 1000 + time_diff.microseconds / 1000      # 毫秒级时间差
    logger.info("Training time: {} ms, {} s, {} min", milliseconds, time_diff.seconds, time_diff.seconds / 60)

    # save model
    time_stamp = time.strftime("%y%m%d-%H%M",time.localtime())
    model_name ="{}_{}_{}_svm_joblib.model".format(time_stamp, app, vect)
    joblib.dump(clf, model_name)

    # predict
    logger.debug("Prediction begin ...")
    start_time = datetime.now()
    predict_label = clf.predict(test_data)
    end_time = datetime.now()
    time_diff = end_time - start_time                                            # 时间差
    milliseconds = time_diff.seconds * 1000 + time_diff.microseconds / 1000      # 毫秒级时间差
    logger.info("Predict time: {} ms, {} s, {} min", milliseconds, time_diff.seconds, time_diff.seconds / 60)

    # save predict lables to file
    time_stamp = time.strftime("%y%m%d-%H%M",time.localtime())
    save_label(predict_label, f"{time_stamp}_{app}_predict.label")

    # evaluate the predict result
    logger.debug("Evaluating ...")
    fig_name = "{}_{}_{}_svm_confusion_matrix.png".format(time_stamp, app, vect)
    metric_sklearn = evaluate_sklearn(predict_label, test_label, fig_name)
    
    # write the evaluation result into file
    write_evaluation_result('SVM', app, vect, metric_sklearn)
    

# train svm with grid search
# def train_svm_grid_search():
#     C_range = [0.1, 1, 10, 100, 1000, 10000, 100000]
#     gamma_range = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100]
#     param_grid = dict(gamma=gamma_range, C=C_range)
    
#     # load all samples and divide them into train set, test set and validation set based on the proportion -- 6:3:1
#     d_instance = data()
#     train_data, test_data, val_data, train_label, test_label, val_label = d_instance.get_train_test_val_set()

#     # grid search and train SVM
#     logger.debug("Start grid search ...")
#     clf = svm.SVC(decision_function_shape='ovr', class_weight="balanced")
#     grid = GridSearchCV(clf, param_grid, refit = True, cv = 5, verbose=2, n_jobs=50)
#     grid.fit(train_data, train_label)
#     logger.info("Best estimator: {}", grid.best_estimator_)
#     logger.info("Best parameters: {}, best score: {}", grid.best_params_, grid.best_score_)

#     # using test set to predict
#     logger.debug("Prediction begin ...")
#     predict_label = grid.predict(test_data)

#     # evaluate the predict result
#     logger.debug("Evaluating ...")
#     metric_sklearn = evaluate_sklearn(predict_label, test_label, "svm_confusion_matrix.png")

#     # write the evaluation result into file
#     write_evaluation_result(metric_sklearn)


# test
# def validate():
#     val_data_file = "../../../dataset/serialization/validate.data"
#     val_data = np.fromfile(val_data_file, dtype=np.int8).reshape((-1, 500))
#     label_list = 6 * [0] + 6 * [1] + 6 * [2] + 6 * [3] + 6 * [4] + 6 * [5]
#     val_label = np.array(label_list, dtype=np.int8)

#     logger.debug("Validation begin ...")
#     logger.info("data size: {}, label size: {}", np.shape(val_data), np.shape(val_label))
#     logger.debug("Actual label: {}", val_label)
#     # load svm model
#     clf = joblib.load("svm.joblib.model")
#     # predict
#     logger.debug("Predicting ...")
#     predict_label = clf.predict(val_data)
#     logger.debug("Predict label: {}", predict_label)
#     # evaluate
#     logger.debug("Evaluating ...")
#     metric_sklearn = evaluate_sklearn(predict_label, val_label, "val_cm.png")


if __name__ == "__main__":
    logger.add("svm.log")

    # "web_app" or "wordpress"
    app = "wordpress"
    # "albert" or "int"
    vect = "albert"
    train_svm(app, vect)
    
    #train_svm_grid_search()
    # d_instance = data()
    # train_data, test_data, val_data, train_label, test_label, val_label = d_instance.get_train_test_val_set()
    # validate()
