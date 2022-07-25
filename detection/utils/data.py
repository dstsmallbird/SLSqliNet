import torch
import numpy as np
from loguru import logger
from tensorflow import convert_to_tensor, reshape
from sklearn.model_selection import train_test_split

from .config import config

class data:
    def __init__(self, app, gpu_index):
        self.device = torch.device('cuda:' + str(gpu_index)) if torch.cuda.is_available() and gpu_index != -1 else torch.device('cpu')
        self.app = app
        self.train_prop = config["model"]["train_proportion"]
        self.test_prop = config["model"]["test_proportion"]
        self.val_prop = config["model"]["val_proportion"]

        self.val_test_prop = self.test_prop + self.val_prop
        self.val_ = self.val_prop / self.val_test_prop
        self.test_ = self.test_prop / self.val_test_prop

        self.dim = config["datasets"]["dimension"]
        self.albert_dim = config["datasets"]["albert_dimension"]

        logger.debug("Initialize data loading")


    @logger.catch
    def get_data(self):
        X = []              # all samples of 6 datasets(time_blind, bool_blind, illegal, tautology, union, normal)
        y = []              # all labels of 6 datasets(time_blind, bool_blind, illegal, tautology, union, normal)
        sample_count = 0    # store the size of X

        # load all datasets of different categories
        for dataset in config["datasets"][self.app]:
            X.extend(np.fromfile(dataset["file"], dtype=np.int8).reshape((-1, self.dim)))
            # X.extend(np.load(dataset["file"], allow_pickle=True).tolist())
            # get the size of current dataset
            dataset_size = len(X) - sample_count
            sample_count = len(X)
            y += dataset_size * [dataset["label"]]
            logger.info('dataset type: {}, file path: {}, size: {}, current samples size: {}', dataset["type"], dataset["file"], dataset_size, np.shape(X))
        
        X = np.array(X, dtype=np.int8)
        y = np.array(y, dtype=np.int8)
        print(type(X),type(X[0]))
        print(type(y),type(y[0]))
        logger.info('total size of samples: {}, total size of labels: {}', len(X), len(y))
        
        # split samples and labels into train set, validation set and test set
        logger.info("train proportion: {}, test proportion: {}, validation proportion: {}", self.train_prop, self.test_prop, self.val_prop)
        train_data, val_test_data, train_label, val_test_label = train_test_split(X, y, random_state = 49, train_size = self.train_prop, test_size = self.val_test_prop, shuffle = True)
        test_data, val_data, test_label, val_label = train_test_split(val_test_data, val_test_label, random_state = 49, train_size = self.test_, test_size = self.val_, shuffle = True)
        logger.info(
            'train data size: {}, train labels size: {}, test data size: {}, test labels size: {}, validation data size: {}, validation labels size: {}',
            np.shape(train_data),
            np.shape(train_label),
            np.shape(test_data),
            np.shape(test_label),
            np.shape(val_data),
            np.shape(val_label)
        )
        # self.save_train_test_val_set(train_data, test_data, val_data, train_label, test_label, val_label)
        return train_data, test_data, val_data, train_label, test_label, val_label
    
    @logger.catch
    def save_train_test_val_set(self, train_data, test_data, val_data, train_label, test_label, val_label):
        logger.debug("save train set, test set and validation set ...")
        # train set
        train_data_file = config["train_set"][self.app]["data"]
        train_label_file = config["train_set"][self.app]["label"]
        # test set
        test_data_file = config["test_set"][self.app]["data"]
        test_label_file = config["test_set"][self.app]["label"]
        # validation set
        val_data_file = config["val_set"][self.app]["data"]
        val_label_file = config["val_set"][self.app]["label"]

        print(type(train_data), type(train_label))
        print(type(train_data[0]), type(train_label[0]))
        
        train_data.tofile(train_data_file)
        train_label.tofile(train_label_file)
        logger.info("train set size: {}, label size: {}", np.shape(train_data), np.shape(train_label))
        logger.info("train set file: {}, label file: {}", train_data_file, train_label_file)
        
        test_data.tofile(test_data_file)
        test_label.tofile(test_label_file)
        logger.info("test set size: {}, label size: {}", np.shape(test_data), np.shape(test_label))
        logger.info("test set file: {}, label file: {}", test_data_file, test_label_file)
        
        val_data.tofile(val_data_file)
        val_label.tofile(val_label_file)
        logger.info("val set size: {}, label size: {}", np.shape(val_data), np.shape(val_label))
        logger.info("val set file: {}, label file: {}", val_data_file, val_label_file)


    @logger.catch
    def get_train_test_val_set(self):
        # train set
        train_data_file = config["train_set"][self.app]["data"]
        train_label_file = config["train_set"][self.app]["label"]
        # test set
        test_data_file = config["test_set"][self.app]["data"]
        test_label_file = config["test_set"][self.app]["label"]
        # val set
        val_data_file = config["val_set"][self.app]["data"]
        val_label_file = config["val_set"][self.app]["label"]
        
        # dimension of one sample
        dim = self.dim

        train_data = np.fromfile(train_data_file, dtype=np.int8).reshape((-1, dim))
        train_label = np.fromfile(train_label_file, dtype=np.int8)

        test_data = np.fromfile(test_data_file, dtype=np.int8).reshape((-1, dim))
        test_label = np.fromfile(test_label_file, dtype=np.int8)

        val_data = np.fromfile(val_data_file, dtype=np.int8).reshape((-1, dim))
        val_label = np.fromfile(val_label_file, dtype=np.int8)
        
        logger.debug("[APP]: {}", self.app)
        logger.info(
            'train data size: {}, train labels size: {}, test data size: {}, test labels size: {}, validation data size: {}, validation labels size: {}',
            np.shape(train_data),
            np.shape(train_label),
            np.shape(test_data),
            np.shape(test_label),
            np.shape(val_data),
            np.shape(val_label)
        )
        return train_data, test_data, val_data, train_label, test_label, val_label


    @logger.catch
    def get_word_embedding_data(self):
        X = []              # all samples of 6 datasets(time_blind, bool_blind, illegal, tautology, union, normal)
        y = []              # all labels of 6 datasets(time_blind, bool_blind, illegal, tautology, union, normal)
        sample_count = 0    # the size of X

        # load all datasets of different categories
        for dataset in config["datasets"][self.app]:
            
            if dataset["type"] == "time blind":
                X = torch.load(dataset["albert_file"], map_location=self.device)
            elif dataset["type"] == "union" or dataset["type"] == "normal":
                file_list = dataset["albert_file"]
                for file in file_list:
                    X = torch.cat((X, torch.load(file, map_location=self.device)))
            else:
                X = torch.cat((X, torch.load(dataset["albert_file"], map_location=self.device)))

            # get the size of current dataset
            dataset_size = len(X) - sample_count
            sample_count = len(X)
            y += dataset_size * [dataset["label"]]
            logger.info('type: {}, file path: {}, size: {}, current samples size: {}', dataset["type"], dataset["file"], dataset_size, X.size())
        
        y = torch.tensor(y, dtype=torch.int8)
        logger.info('total size of samples: {}, total size of labels: {}', len(X), len(y))
        
        # split samples and labels into train set, validation set and test set
        logger.info("train proportion: {}, test proportion: {}, validation proportion: {}", self.train_prop, self.test_prop, self.val_prop)
        train_data, val_test_data, train_label, val_test_label = train_test_split(X, y, random_state = 49, train_size = self.train_prop, test_size = self.val_test_prop, shuffle = True)
        test_data, val_data, test_label, val_label = train_test_split(val_test_data, val_test_label, random_state = 49, train_size = self.test_, test_size = self.val_, shuffle = True)
        logger.info(
            'train data size: {}, train labels size: {}, test data size: {}, test labels size: {}, validation data size: {}, validation labels size: {}',
            train_data.size(),
            train_label.size(),
            test_data.size(),
            test_label.size(),
            val_data.size(),
            val_label.size()
        )
        # self.save_train_test_val_set(train_data, test_data, val_data, train_label, test_label, val_label)
        return train_data, test_data, val_data, train_label, test_label, val_label


    @logger.catch
    def save_word_embedding_train_test_val_set(self, train_data, test_data, val_data, train_label, test_label, val_label):
        # train set
        train_data_file_list = config["train_set"][self.app]["albert_data"]
        train_label_file_list = config["train_set"][self.app]["albert_label"]
        # test set
        test_data_file_list = config["test_set"][self.app]["albert_data"]
        test_label_file_list = config["test_set"][self.app]["albert_label"]
        # validation set
        val_data_file_list = config["val_set"][self.app]["albert_data"]
        val_label_file_list = config["val_set"][self.app]["albert_label"]

        files = [
            [train_data_file_list, train_label_file_list],
            [test_data_file_list, test_label_file_list],
            [val_data_file_list, val_label_file_list]
        ]
        data = [
            [train_data, train_label],
            [test_data, test_label],
            [val_data, val_label]
        ]

        for pair in range(0, 3):
            pointer = 0
            file_count = len(files[pair][0])

            for file_ids in range(0, file_count):
                data_file = files[pair][0][file_ids]
                label_file = files[pair][1][file_ids]
                logger.debug("[Pointer] {}, [Data File] {}, [Label File] {}".format(pointer, data_file, label_file))
                # save 15000 samples
                torch.save(data[pair][0][pointer : pointer + 15000].clone().detach().requires_grad_(False), data_file)
                # save 15000 labels
                torch.save(data[pair][1][pointer : pointer + 15000].clone().detach().requires_grad_(False), label_file)
                # set pointer
                pointer = pointer + 15000


    @logger.catch
    def get_word_embedding_train_test_val_set(self):
        # train set
        train_data_file_list = config["train_set"][self.app]["albert_data"]
        train_label_file_list = config["train_set"][self.app]["albert_label"]
        # test set
        test_data_file_list = config["test_set"][self.app]["albert_data"]
        test_label_file_list = config["test_set"][self.app]["albert_label"]
        # val set
        val_data_file_list = config["val_set"][self.app]["albert_data"]
        val_label_file_list = config["val_set"][self.app]["albert_label"]

        files = [
            [train_data_file_list, train_label_file_list],
            [test_data_file_list, test_label_file_list],
            [val_data_file_list, val_label_file_list]
        ]
        # 0 - train_data, 1 - train_label, 2 - test_data, 3 - test_label, 4 - val_data, 5 - val_label
        result = []

        for pair in files:
            data = []
            label = []
            file_count = len(pair[0])

            for file_ids in range(0, file_count):
                data_file = pair[0][file_ids]
                label_file = pair[1][file_ids]
                logger.debug('[data file] {} [size] {}', data_file, torch.load(data_file, map_location=self.device).size())

                if file_ids == 0:
                    data = torch.load(data_file, map_location=self.device)
                    label = torch.load(label_file, map_location=self.device)
                else:
                    data = torch.cat((data, torch.load(data_file, map_location=self.device)))
                    label = torch.cat((label, torch.load(label_file, map_location=self.device)))
            
            result.append(data)
            result.append(label)
        
        logger.debug("[APP]: {}", self.app)
        logger.info(
            'train data size: {}, train labels size: {}, test data size: {}, test labels size: {}, validation data size: {}, validation labels size: {}',
            result[0].size(),
            result[1].size(),
            result[2].size(),
            result[3].size(),
            result[4].size(),
            result[5].size()
        )
        # return train_data, test_data, val_data, train_label, test_label, val_label
        return result[0], result[2], result[4], result[1], result[3], result[5]

    
    @logger.catch
    def get_tf_albert_dataset(self, reshape_flag, batch_size):
        train_data, test_data, val_data, train_label, test_label, val_label = self.get_word_embedding_train_test_val_set()
        logger.debug("Convert to tensorflow tensor")

        if batch_size != 0:
            logger.debug("Cut dataset based on batch size, batch_size: {}", batch_size)

            # calculate remainder of train dataset and validation dataset
            train_remainder = len(train_data) % batch_size
            # test_remainder = len(test_data) % batch_size
            val_remainder = len(val_data) % batch_size
            logger.info("Cut train data: {}, cut validation data: {}", train_remainder, val_remainder)
            
            # calculate quantity to be retained
            train_qtt = len(train_data)-train_remainder
            # test_qtt = len(test_data)-test_remainder
            val_qtt = len(val_data)-val_remainder
            
            # cut dataset and convert to tensorflow tensor from torch tensor
            train_data = convert_to_tensor( train_data.cpu().numpy()[:train_qtt] )
            train_label = convert_to_tensor( train_label.cpu().numpy()[:train_qtt] )
            val_data = convert_to_tensor( val_data.cpu().numpy()[:val_qtt] )
            val_label = convert_to_tensor( val_label.cpu().numpy()[:val_qtt] )

            test_label = convert_to_tensor( test_label.cpu().numpy() )
            test_data = convert_to_tensor( test_data.cpu().numpy() )
        else:    
            #convert to tensorflow tensor from torch tensor
            train_data = convert_to_tensor(train_data.cpu().numpy())
            test_data = convert_to_tensor(test_data.cpu().numpy())
            val_data = convert_to_tensor(val_data.cpu().numpy())
            train_label = convert_to_tensor(train_label.cpu().numpy())
            test_label = convert_to_tensor(test_label.cpu().numpy())
            val_label = convert_to_tensor(val_label.cpu().numpy())

        # reshape dataset to 3D from 2D
        if reshape_flag == True:
            train_data = reshape(train_data, (len(train_data), 1, 768))
            test_data = reshape(test_data, (len(test_data), 1, 768))
            val_data = reshape(val_data, (len(val_data), 1, 768))

        logger.info(
            'train data size: {}, train labels size: {}, test data size: {}, test labels size: {}, validation data size: {}, validation labels size: {}',
            train_data.shape,
            train_label.shape,
            test_data.shape,
            test_label.shape,
            val_data.shape,
            val_label.shape
        )

        return train_data, test_data, val_data, train_label, test_label, val_label

