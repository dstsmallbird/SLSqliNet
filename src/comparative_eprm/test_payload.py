import re
import numpy as np
from loguru import logger
from sklearn.model_selection import train_test_split

# get all payload samples from file and generate the corresponding labels
def get_data(abnormal_list, normal_list):
    X = []              # all samples of 6 datasets(time_blind, bool_blind, illegal, tautology, union, normal)
    Y = []              # all labels of 6 datasets(time_blind, bool_blind, illegal, tautology, union, normal)
    sample_count = 0    # store the size of X

    # get all abnormal payload(time_blind, bool_blind, illegal, tautology, union)
    for abnormal_file in abnormal_list:
        line_count = 0  # the count of payloads in file
        
        with open(abnormal_file, 'r') as f_read:
            for line in f_read:
                line_count += 1
                X.append(line)
        
        Y += line_count * [1]   # label of abnormal sample is 1
        sample_count += line_count
        logger.info("[Abnormal] Read file: {}, payload count: {}", abnormal_file, line_count)

    # get all normal payload
    for normal_file in normal_list:
        line_count = 0  # the count of payloads in file
        
        with open(normal_file, 'r') as f_read:
            for line in f_read:
                line_count += 1
                X.append(line)
        
        Y += line_count * [0]   # label of normal sample is 0
        sample_count += line_count
        logger.info("[normal] Read file: {}, payload count: {}", normal_file, line_count)
    
    logger.info("All sample count: {}, length of X: {}, length of Y: {}", sample_count, len(X), len(Y))
    return X, Y


# shuffle and divided all payload into trian data and test data
def shuffle_split(X, Y, train_prop):
    test_prop = round(1 - train_prop, 10)
    train_data, test_data, train_label, test_label = train_test_split(X, Y, random_state = 79, train_size = train_prop, test_size = test_prop, shuffle = True)
    
    logger.info("train proportion: {}, test proportion: {}", train_prop, test_prop)
    logger.info(
        'train data size: {}, train labels size: {}, test data size: {}, test labels size: {}',
        len(train_data),
        len(train_label),
        len(test_data),
        len(test_label)
    )
    return train_data, test_data, train_label, test_label


# 从恶意样本中提取一部分作为对比实验wordpress组的恶意样本，返回混淆的样本和标签
def split_abnormal(abnormal_list, invalid_prop):
    X = []              # all samples of abnormal datasets(time_blind, bool_blind, illegal, tautology, union)
    Y = []              # label
    sample_count = 0    # store the size of X

    # get all abnormal payload(time_blind, bool_blind, illegal, tautology, union)
    for abnormal_file in abnormal_list:
        line_count = 0  # the count of payloads in file
        
        with open(abnormal_file, 'r') as f_read:
            for line in f_read:
                line_count += 1
                X.append(line)
        
        Y += line_count * [1]   # label of abnormal sample is 1
        sample_count += line_count
        logger.info("[Abnormal] Read file: {}, payload count: {}", abnormal_file, line_count)
    
    logger.debug("[Split Abnormal Dataset ...] invalid dataset prop: {}", invalid_prop)
    invalid_data, valid_data, invalid_label, valid_label = shuffle_split(X, Y, invalid_prop)
    
    return valid_data, valid_label

# 读取正常样本文件获取正常样本，切分恶意样本，保存测试集
def get_wordpress_data(abnormal_list, normal_list, invalid_prop):
    X = []              # all samples of normal datasets
    Y = []              
    sample_count = 0    # store the size of X

    # get all normal payload
    for normal_file in normal_list:
        line_count = 0  # the count of payloads in file
        
        with open(normal_file, 'r') as f_read:
            for line in f_read:
                line_count += 1
                X.append(line)
        
        Y += line_count * [0]   # label of normal sample is 0
        sample_count += line_count
        logger.info("[normal] Read file: {}, payload count: {}", normal_file, line_count)
    
    abnormal_data, abnormal_label = split_abnormal(abnormal_list, invalid_prop)
    logger.debug("Abnormal data/label size: {}/{}, normal data/label size: {}/{}", np.shape(abnormal_data), np.shape(abnormal_label), np.shape(X), np.shape(Y))
    X.extend(abnormal_data)
    Y.extend(abnormal_label)
    
    logger.info("All sample count: {}, length of X: {}, length of Y: {}", sample_count+len(abnormal_data), len(X), len(Y))
    return X, Y

# save shuffled payloads and labels into file
def save_to_file(shuffled_data, shuffled_label, data_file, label_file):
    # convert to numpy array
    shuffled_label = np.array(shuffled_label, dtype=np.int8)

    # save payloads
    with open(data_file, 'w') as f_data:
        count = 0
        for payload in shuffled_data:
            count += 1

            if re.search(r'\n$', payload):
                f_data.write(payload)
            else:
                f_data.write(payload + '\n')
                logger.warning("Wrong line {} without 'CRLF' in the end. Fixed.", count)
            
    # logger.debug("Shuffled data/label size: {}/{}", np.shape(shuffled_data), np.shape(shuffled_label))
    
    # save labels by using numpy
    shuffled_label.tofile(label_file)
    logger.info("Save shuffled payload data to file[TXT]: {}", data_file)
    logger.info("Save shuffled labels to file[Numpy.tofile]: {}", label_file)


if __name__ == '__main__':
    ABNORMAL_PATH = '../../dataset/payload/'
    NORMAL_PATH = '../../dataset/comparative_eprm/'
    OUTPUT_PATH = '../../dataset/comparative_eprm/'
    ABNORMAL_CLASSES = ["time_blind", "bool_blind", "illegal", "tautology", "union"]
    TRAIN_PROP = 0.7
    invalid_prop = 0.82    # 1-13335/74555

    # web_app
    web_app_abnormal_list = [ ABNORMAL_PATH + abnormal_class + '.txt' for abnormal_class in ABNORMAL_CLASSES ]
    web_app_normal_list = [ NORMAL_PATH + 'web_app/normal.txt' ]
    web_app_test_data = OUTPUT_PATH + 'web_app/test_set.txt'
    web_app_test_label = OUTPUT_PATH + 'web_app/test_set.label'

    # wordpress
    wordpress_abnormal_list = [ ABNORMAL_PATH + abnormal_class + '.txt' for abnormal_class in ABNORMAL_CLASSES ]
    wordpress_normal_list = [ NORMAL_PATH + 'wordpress/normal.txt' ]
    wordpress_test_data = OUTPUT_PATH + 'wordpress/test_set.txt'
    wordpress_test_label = OUTPUT_PATH + 'wordpress/test_set.label'
    

    # # web_app
    # X, Y = get_data(web_app_abnormal_list, web_app_normal_list)
    # train_data, test_data, train_label, test_label = shuffle_split(X, Y, TRAIN_PROP)
    # save_to_file(test_data, test_label, web_app_test_data, web_app_test_label)
    
    # wordpress
    test_data, test_label = get_wordpress_data(wordpress_abnormal_list, wordpress_normal_list, invalid_prop)
    save_to_file(test_data, test_label, wordpress_test_data, wordpress_test_label)