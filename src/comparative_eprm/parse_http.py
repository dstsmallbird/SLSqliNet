import re
from loguru import logger

def get_key_value(log_file_list):
    key_value_pairs = []
    for log_file in log_file_list:
        with open(log_file) as f_read:
            reg1 = re.compile(r'"[A-Z]* .*\?(.*) HTTP/1.1"')    # 形如["GET /path?key=value HTTP/1.1"]
            reg2 = re.compile(r'"\w*://.*\?([^"]*)"')           # 形如["protocol://ip/path?key=value"]
            
            for line in f_read:
                a = re.search(reg1, line)
                b = re.search(reg2, line)
                if a:
                    key_value_pairs.append(a.groups(1)[0])      # groups 获取匹配到的元组，返回一个元组
                if b:
                    key_value_pairs.append(b.groups(1)[0])      # 获取匹配到的元组
    
    logger.debug("key value pairs counts: {}", len(key_value_pairs))
    return key_value_pairs


def parse_value(key_value_pairs, output_file):
    values = []
    for line in key_value_pairs:
        key_value_arr = line.split('&')     # 得到一个列表，每个元素是 'key=value', 也有不含等号的字符串
        
        for item in key_value_arr:
            if '=' in item:
                va = item.split('=')[1]     # 每个 key=value 对被拆分成 key 和 value，保存value
                # value非空
                if va:
                    values.append(va) 
    
    logger.debug("count of values: {}", len(values))
    save_to_file(values, output_file)


def save_to_file(values, output_file):
    with open(output_file, 'w') as f_write:
        for va in values:
            f_write.write(va + '\n')
    logger.info("Saved to file: {}", output_file)


def get_url(log_file_list):
    url_list = []
    for log_file in log_file_list:
        with open(log_file) as f_read:
            reg1 = re.compile(r'"[A-Z]* (.*\?.*) HTTP/1.1"')                   # 形如["GET /path?key=value HTTP/1.1"]
            reg2 = re.compile(r'"\w*://\d+\.\d+\.\d+\.\d+(/.*\?[^"]*)"')       # 形如["protocol://ip/path?key=value"]
            # reg1 = re.compile(r'"[A-Z]* .*\?(.*) HTTP/1.1"')    # 形如["GET /path?key=value HTTP/1.1"]
            # reg2 = re.compile(r'"\w*://.*\?([^"]*)"')           # 形如["protocol://ip/path?key=value"]
            
            for line in f_read:
                a = re.search(reg1, line)
                b = re.search(reg2, line)
                if a:
                    url_list.append(a.groups(1)[0])      # groups 获取匹配到的元组，返回一个元组
                if b:
                    url_list.append(b.groups(1)[0])      # 获取匹配到的元组
    
    logger.debug("url counts: {}", len(url_list))
    return url_list


def extend_url(url_list):
    extend_list = []
    for url in url_list:
        key_value_count = url.count('&')
        extend_list += key_value_count * [url]
    
    url_list += extend_list
    logger.debug("extended url counts: {}", len(url_list))
    return url_list



if __name__ == '__main__':
    dir = '../../dataset/http/'
    http_log = [dir + 'access_log-20211212', dir + 'access_log-20211219', dir + 'access_log-20211229']
    output_file = '../../dataset/comparative_eprm/wordpress/normal.txt'

    url_list = get_url(http_log)
    url_list = extend_url(url_list)
    save_to_file(url_list, "../../dataset/comparative_eprm/wordpress/normal_url.txt")

    # key_value_pairs = get_key_value(http_log) 
    # parse_value(key_value_pairs, output_file)