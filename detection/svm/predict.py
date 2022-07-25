import numpy as np
import sys
from datetime import datetime
import joblib
import torch
from loguru import logger

sys.path.append("../")
# from utils.data import data
from utils.evaluate import evaluate_sklearn
# from utils.evaluate import write_evaluation_result
from utils.config import config


DEVICE = torch.device('cpu')
normal_samples = torch.tensor([])
predict_label_file = "./normal_dataset_predict.label"
wordpress_svm_model = joblib.load('220513-1515_wordpress_albert_svm_joblib.model')


# 读取正常样本
for file in config["datasets"]["wordpress"][5]["albert_file"]:
    normal_samples = torch.cat((normal_samples, torch.load(file, map_location=DEVICE)))
logger.info("[Wordpress] Normal samples count: {}", normal_samples.shape)

# 创建真实标签
actual_label = np.array(len(normal_samples) * [5])
logger.info("Actual labels count: {}", np.shape(actual_label))

# 预测
logger.debug("Predicting ...")
start_time = datetime.now()
predict_label = wordpress_svm_model.predict(normal_samples.detach().numpy()) # 得到预测标签
end_time = datetime.now()
time_diff = end_time - start_time                                            # 时间差
milliseconds = time_diff.seconds * 1000 + time_diff.microseconds / 1000      # 毫秒级时间差
logger.info("Predict time: {} ms, {} s, {} min", milliseconds, time_diff.seconds, time_diff.seconds / 60)

# 保存预测标签
logger.info("Save predict label to file: {}", predict_label_file)
predict_label = np.array(predict_label, dtype=np.int8)
predict_label.tofile(predict_label_file)

# 评估
logger.debug("Evaluating ...")
evaluate_sklearn(predict_label, actual_label, 'test.png')