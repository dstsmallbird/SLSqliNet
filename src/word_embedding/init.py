import os

# configure gpu device
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICE']='7'

from loguru import logger
from albert_embedding import Pretrain


logger.add("pretrain.log")
logger.debug("Pretrain begin ...")
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
    
instance = Pretrain()
# web_app
instance.iterate_word_embedding(input_file_web_app[5], output_file_web_app[5])
# wordpress
for i in range(0,6):
    instance.iterate_word_embedding(input_file_wordpress[i], output_file_wordpress[i])
