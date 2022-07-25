import re
import random
from loguru import logger

# step 1 - 去除开头出现 [\w)))]、[(]、[字符串,] 形式的 payload
def del_line(line_number, line):
    # 符合 [\w)))]、[(]、[字符串,] 形式时，返回 True，令调用函数丢弃当前行，否则返回 False，表示保留该行
    if re.search(r'^[-%\._\w]*\){3}', line) or re.search(r'^\(', line) or re.search(r'^[-%\._\w]+,', line):
        logger.debug("[{}]-[Del] {}", line_number, line)
        return True
    
    return False


# step 2 - 转换双引号为单引号
def convert_to_single_quote(line_number, line):
    # 存在双引号时，转双引号 -> 单引号
    if re.search(r'"', line):
        line = re.sub(r'"', "'", line)
        logger.debug("[{}]-[Single quote] {}", line_number, line)
    
    return line


# step 3 - 去除 payload 前端的正常输入
def del_normal(line_number, line):
    # [str ] -> [ ]
    line = re.sub(r'^[-%\._\w]* ', ' ', line)
    # [str'] -> [']
    line = re.sub(r'^[-%\._\w]*\'', "'", line)
    # [str)] -> [)]
    line = re.sub(r'^[-%\._\w]*\)', ")", line)
    # [str;] -> [;]
    line = re.sub(r'^[-%\._\w]*;', ";", line)
    # [str/*] -> [/*]
    line = re.sub(r'^[-%\._\w]*/\*', '/*', line)

    return line


# step 4 - 向包含 [SELECT 8928 WHERE 9001=9001] 的 payload 补充 FROM DUAL
def add_dual(line_number, line):
    if re.search(r'select \'?\w{4}\'? where \d{4}=\d{4}', line, re.IGNORECASE):
        rand_num = random.randint(1000, 9999)
        sub_str = "FROM DUAL WHERE {}={}".format(rand_num, rand_num)
        line = re.sub('WHERE \d{4}=\d{4}', sub_str, line, flags=re.I)
        logger.debug("[{}]-[Dual] {}", line_number, line)
    
    return line


# step 5 - determine whether payload contains annotator[-- |#]
def has_comment(line):
    if re.search(r'(-- |#).*$', line):
        return True
    return False


# step 6 - determine whether payload is closed
def is_closed(line):
    # begin with [')))]
    if re.search(r"^'\){3}", line):
        if re.search(r"\({3}\'\w{4}\'(=|\s?like\s?)\'\w{4}$", line, flags=re.I):
            return True
    # begin with ['))]
    elif re.search(r"^'\){2}", line):
        if re.search(r"\({2}\'\w{4}\'(=|\s?like\s?)\'\w{4}$", line, flags=re.I):
            return True
    # begin with [')]
    elif re.search(r"^'\)", line):
        if re.search(r"\(\'\w{4}\'(=|\s?like\s?)\'\w{4}$", line, flags=re.I):
            return True
    # begin with ['] only
    elif re.search(r"^'[^\)]", line):
        if re.search(r"\'\w{4}\'(=|\s?like\s?)\'\w{4}$", line, flags=re.I) or re.search(r"'$", line):
            return True
    # begin with [)))]
    elif re.search(r"^\){3}", line):
        if re.search(r"\({3}\w{4}(=|\s?like\s?)\w{4}$", line, flags=re.I):
            return True
    # begin with [))]
    elif re.search(r"^\){2}", line):
        if re.search(r"\({2}\w{4}(=|\s?like\s?)\w{4}$", line, flags=re.I):
            return True
    # begin with [)]
    elif re.search(r"^\)", line):
        if re.search(r"\(\w{4}(=|\s?like\s?)\w{4}$", line, flags=re.I):
            return True
    
    return  False


# input file to processing
def file_process(raw_file, out_file_comment, out_file_no_comment):
    with open(out_file_comment, 'w') as f_w_comment:
        with open(out_file_no_comment, 'w') as f_w_no_comment:
            with open(raw_file, 'r') as f_read:
                line_number = 0     # initialize line number
                
                for line in f_read:
                    line_number += 1
                    
                    # step 1 - determine current line whether need to delete
                    if del_line(line_number, line) == False:
                        # step 2 - convert double-quote to single-quote
                        line = convert_to_single_quote(line_number, line)
                        # step 3 - delete the normal part at the beginning of payload
                        line = del_normal(line_number, line)
                        # step 4 - add [from dual] into sql like [SELECT 8928 WHERE 9001=9001]
                        line = add_dual(line_number, line)
                        # step 5 - determine whether payload contains annotator, and write the payload to different file
                        if has_comment(line):
                            f_w_comment.write(line)
                        # step 6 - determine whether payload is closed
                        elif re.search(r"^['\)]", line):
                            if is_closed(line):
                                f_w_no_comment.write(line)
                        else:
                            f_w_no_comment.write(line)
                                

if __name__ == '__main__':
    raw_path = '../../dataset/payload/'
    out_path = '../../dataset/payload//wordpress/'
    type_list = ['time_blind', 'bool_blind', 'illegal', 'tautology', 'union']
    # read TXT files in raw_path directory
    raw_file_list = [raw_path + item + '.txt' for item in type_list]
    # write to TXT files in [./wordpress] directory
    out_file_comment = [out_path + item + '_comment.txt' for item in type_list]   # payload contains [-- |#]
    out_file_no_comment = [out_path + item + '_no_comment.txt' for item in type_list]   # payload has no annotator

    # 0-time_blind, 1-bool_blind, 2-illegal, 3-tautology, 4-union
    index = 4

    log_file = out_path + type_list[index] + "_wordpress.log"
    logger.add(log_file)
    logger.info("Raw file:{}, output file: {}, {}", raw_file_list[index], out_file_comment[index], out_file_no_comment[index])
    
    file_process(raw_file_list[index], out_file_comment[index], out_file_no_comment[index])
