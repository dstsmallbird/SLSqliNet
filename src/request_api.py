"""
Read files to get the SQL injection payload and request the API through POST method
"""
import requests
import random
from tqdm import tqdm
from name import NAME

files = [
    ["/root/app/expand/tautology_expand.txt","/root/app/tautology.txt"],    # tautology
    ["/root/app/expand/illegal_expand.txt","/root/app/illegal.txt"],        # illegal
    ["/root/app/expand/union_expand.txt","/root/app/union.txt"],            # union
    ["/root/app/expand/bool_blind_expand.txt","/root/app/bool_blind.txt"],  # bool_blind
    ["/root/app/expand/time_blind_expand.txt","/root/app/time_blind.txt"],  # time_blind
]

# sql_type: 0 - tautology, 1 - illegal, 2 - union, 3 - bool_blind, 4 - time_blind, 5 - normal
# is_formal: 1 - formal requests, 0 - other requests
def request(sql_type, is_formal):
    """
    perform sql injection
    """
    url = "http://localhost:8888/test"
    # line number
    count = 0
    file = files[sql_type][is_formal]

    with open(file,'r') as f:
        for line in f:
            line = line.strip('\n')
            count += 1
            # submit POST parameters
            data = {"user":line,"count":count,"formal":is_formal,"type":sql_type}
            response = requests.post(url,data=data)
            print(response.text)


# sql_type: 0 - tautology, 1 - illegal, 2 - union, 3 - bool_blind, 4 - time_blind, 5 - normal
# is_formal: 1 - formal requests, 0 - other requests
def request_normal_api():
    """
    perform normal request
    """
    normal_url = 'http://localhost:8888/normal'
    is_formal = 1
    sql_type = 5
    
    # request api using the above POST data dictionary at least 75,000 times
    for count in tqdm(range(1, 75001)):
        # generate random parameter
        rand_int = random.randint(0, 10000)
        rand_col = random.choice(['user_id', 'group_id', 'fullname', 'user_nickname', 'display_name', 'user_email', 'password', 'rights', 'login'])
        rand_str = random.choice(NAME)
        params = random.choice([rand_int, rand_col, rand_str])

        # create POST data dictionary: "params", "count", "formal", "type"
        data = {"params":params, "count":count, "formal":is_formal, "type":sql_type}
        # request "http://host:port/normal" api
        response = requests.post(normal_url, data=data)


if __name__ == '__main__':
    # request(2,1) # union,formal
    request_normal_api()