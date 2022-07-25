'''
get normal payload samples for self-build web app
'''
import sys
import random
from tqdm import tqdm
sys.path.append("../")
from name import NAME

OUTPUT_FILE = '../../dataset/comparative_eprm/web_app/normal.txt'

params_list = []
for count in tqdm(range(75000)):
    # generate random normal payload
    rand_int = random.randint(0, 10000)
    rand_col = random.choice(['user_id', 'group_id', 'fullname', 'user_nickname', 'display_name', 'user_email', 'password', 'rights', 'login'])
    rand_str = random.choice(NAME)
    params_list.append( random.choice([str(rand_int), rand_col, rand_str]) )
    
with open(OUTPUT_FILE, 'w') as f_write:
    for param in params_list:
        f_write.write(param + '\n')