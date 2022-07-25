"""
Pretrain using Albert to get sentence-vector(embedding)
"""
import torch
import os

# configure gpu device
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICE']='7'
gpu_device = torch.device("cuda:7")

from transformers import AlbertTokenizer, AlbertModel
from loguru import logger
from tqdm import tqdm
import numpy as np
import math


class Pretrain:
    def __init__(self):
        # super(Pretrain, self).__init__()

        self.tokenizer = AlbertTokenizer.from_pretrained('albert-base-v2')          # initialize tokenizer
        self.model = AlbertModel.from_pretrained("albert-base-v2").to(gpu_device)   # initialize albert model(albert-base-v2)
        self.embedding_dim = self.model.config.hidden_size                          # dimension of embedding(equals to the dimension of output sentence vector)
        self.batch_size = 10                                                        # predict some samples one time
        self.sample_count = -1

    
    # step 1 - read file to get the sample count
    def set_sample_count(self, file_name):
        count = 0
        with open(file_name, 'r') as f_read:
            for line in f_read:
                count += 1
        self.sample_count = count
        logger.info("[Sample Count] {}", self.sample_count)
 
    
    # step 2 - read file to get generalized samples for tokenizing
    def read_generalized_sample(self, in_file, pointer):
        count = 0           # line number
        sample_list = []    # list of samples from file

        with open(in_file, 'r') as f_read:
            for line in tqdm(f_read):
                if count < pointer:
                    count += 1
                    continue
                elif count >= pointer and count < (pointer + self.batch_size):
                    count += 1
                    sample_list.append(line.strip())
                else:
                    break
            # update pointer
            pointer = count
        
        return sample_list, pointer

    
    # step 3 - word embedding based on Albert
    @logger.catch
    def word_embedding(self, in_file, pointer):
        is_first = True
        pooled_output = torch.empty(1, 768)
        # read file to get 50 samples
        text, new_pointer = self.read_generalized_sample(in_file, pointer)

        for tx in text:
            # tokenize
            input_ids = torch.tensor(self.tokenizer.encode(tx, add_special_tokens=True)).unsqueeze(0).to(gpu_device)
            # cut input_ids
            if len(input_ids[0]) > 512:
                input_ids = input_ids[:, :512]
            # predict
            output = self.model(input_ids)
            if is_first:
                pooled_output = output.pooler_output
                is_first = False
            else:
                pooled_output = torch.cat((pooled_output, output.pooler_output))

        return pooled_output, new_pointer
    

    # iterate to read file for word-embedding
    def iterate_word_embedding(self, in_file, out_file):
        logger.debug("Getting generalized samples from file: {}", in_file)
        logger.info("[Init Pointer] 0")
        pointer = 0     # initialize pointer
       
        # set sample count
        self.set_sample_count(in_file)
        file_count = math.ceil(self.sample_count / 15000) 
        if file_count > 1:
            file_list = [ out_file.split('.data')[0]+'_'+str(i)+'.data' for i in range(0, file_count) ]


        while pointer < self.sample_count:
            # get samples and predict to get word-embedding 
            pooled_output, new_pointer = self.word_embedding(in_file, pointer)

            # reset output file
            if file_count > 1:
                out_file = file_list[pointer // 15000]
            
            # first iteration, save result to file immediately
            if (pointer % 15000) == 0:
                torch.save(pooled_output, out_file)
            # otherwise, load file to concat the new result
            else:
                tmp = torch.load(out_file)
                tmp = torch.cat((tmp, pooled_output))
                torch.save(tmp, out_file)
                logger.info("[Output File] {} [Current Word-Embedding Size] {}", out_file, tmp.size())
            
            # update pointer
            pointer = new_pointer
