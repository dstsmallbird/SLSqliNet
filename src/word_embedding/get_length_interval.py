from transformers import AlbertTokenizer, AlbertModel
import numpy as np
import torch
from tqdm import tqdm

class word_embedding:
    def __init__(self):
        self.text = [
            "select TK_IDTF, TK_IDTF, TK_IDTF from TK_IDTF where TK_IDTF=0 and 0=0 union select TK_F(0,0,0,0,0,0,0,0,0,0,TK_VAR,0,0,0,0,0,0,0,0,0,0,0,0,0,TK_VAR,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,TK_VAR,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,TK_VAR,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,TK_F(),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,TK_VAR,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,TK_VAR,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,TK_VAR,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,TK_VAR,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,TK_F(),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,TK_VAR,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,TK_VAR,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,TK_VAR,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,TK_VAR,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,TK_VAR,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,TK_VAR,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,TK_VAR,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,TK_VAR,0,0)-- TK_C",
            "select TK_IDTF, TK_IDTF from TK_IDTF where TK_IDTF < (select TK_IDTF from TK_IDTF where TK_IDTF not in (select TK_IDTF from TK_IDTF where not exists (select * from TK_IDTF where TK_IDTF=TK_STR))) union all select null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null#TK_C",
            "select * from users"
        ]

        self.length_interval = np.zeros(20,dtype=np.int64)  # 0-99, 100-199, 200-299, 300-399, 400-499, 500-599, 600-699, 700-799, ..., 1900-1999
        self.longest_length = -1
        self.count_exceed_512 = 0
        self.file_with_longes_length = ''
        
        self.tokenizer = AlbertTokenizer.from_pretrained('albert-base-v2')
        self.model = AlbertModel.from_pretrained('albert-base-v2')

    

    def tokenize_text(self):
        encoded_input = self.tokenizer(self.text, return_tensors='pt', padding=True)
        input_ids = encoded_input["input_ids"]

        for ids in input_ids:
            length = len(ids)

            if length > self.longest_length:
                self.longest_length = length
            
            # determine which interval the length of current line belongs to
            self.length_interval[length // 100] += 1
        
        print("length interval: {}".format(self.length_interval))
        print("Encoded Input: {}".format(encoded_input))
        #return encoded_input
        return encoded_input['input_ids']

    
    def predict(self, encoded_input):
        #output = self.model(**encoded_input)
        output = self.model(encoded_input)
        print(output.pooler_output)


    def tokenize_predict(self):
        for tx in self.text:
            #encoded_input = self.tokenizer(tx, return_tensors='pt')
            input_ids = torch.tensor(self.tokenizer.encode(tx, add_special_tokens=True)).unsqueeze(0)
            #print("Encoded Length: {}".format(len(encoded_input['input_ids'][0])))
            print("Input_ids size: {}".format(input_ids.size()))
            if len(input_ids[0]) > 512:
                input_ids = input_ids[:, :512]
                print("Cut input_ids: {}".format(input_ids.size()))
            #output = self.model(encoded_input['input_ids'])
            output = self.model(input_ids)
            print(output.pooler_output)


    def get_tokenized_length(self, in_file):
        with open(in_file, 'r') as f_read:
            print("\n[File Reading ...] {}".format(in_file))
            for line in tqdm(f_read):
                text = line.strip()
                # input_ids is two-dimensional array: [[id, id, ..., id]]
                input_ids = torch.tensor(self.tokenizer.encode(text, add_special_tokens=True)).unsqueeze(0)
                length = len(input_ids[0])
                if length > 512:
                    self.count_exceed_512 += 1
                if length > self.longest_length:
                    self.longest_length = length
                    self.file_with_longes_length = in_file
                self.length_interval[length // 100] += 1
        
        print("[Longest Length] {}\n[File Having Longest Sample] {}\n[Count Exceed 512] {}\n[Length Interval] {}\n".format(self.longest_length, self.file_with_longes_length, self.count_exceed_512, self.length_interval))
                

if __name__ == '__main__':
    class_list = ['time_blind', 'bool_blind', 'illegal', 'tautology', 'union', 'normal']

    # web app
    # 0-time_blind， 1-bool_blind， 2-illegal，3-tautology，4-union, 5-normal
    input_path_web_app = '../../dataset/generalizer/generalized_dataset/web_app/'
    input_file_web_app = [ input_path_web_app + item + '.txt' for item in class_list ] 
    output_path_web_app = '../../dataset/word_embedding/web_app/'
    output_file_web_app = [ output_path_web_app + item + '.data' for item in class_list ] 
        
    # wordpress
    # 0-time_blind， 1-bool_blind， 2-illegal，3-tautology，4-union, 5-normal
    input_path_wordpress = '../../dataset/generalizer/generalized_dataset/wordpress/'
    input_file_wordpress = [ input_path_wordpress + item + '_wp.txt' for item in class_list ] 
    output_path_wordpress = '../../dataset/word_embedding/wordpress/'
    output_file_wordpress = [ output_path_wordpress + item + '_wp.data' for item in class_list ]

    ins = word_embedding()
    for file in input_file_web_app:
        ins.get_tokenized_length(file)
    for file in input_file_wordpress:
        ins.get_tokenized_length(file)
        