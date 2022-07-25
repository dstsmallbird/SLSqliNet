'''
將对比实验中的样本还原成URL或者path?key=value形式
'''
import re
from loguru import logger

# 针对web_app的url还原
def restore_url(raw_file, output_file):
    with open(output_file, 'w') as f_write:
        with open(raw_file, 'r') as f_read:
            # 数值开头
            num = re.compile(r'^[-\d]')  
            # 特殊字符串开头
            param = re.compile(r'^(user_id|group_id|fullname|user_nickname|display_name|user_email|password|rights|login)')
            for line in f_read:

                if re.search(num, line):
                    line = 'test?id=' + line
                elif re.search(param, line):
                    line = 'test?params=' + line
                else:
                    line = 'test?user=' + line
                
                f_write.write(line)


def get_wordpress_url(url_file):
    with open(url_file, 'r') as f_read:
        url_list = f_read.readlines()
    
    return url_list


# 针对WordPress的url还原
def restore_wordpress_test_set(url_file, raw_file, output_file):
    url_list = get_wordpress_url(url_file)
    url_count = len(url_list)
    logger.info("Url count from file: {}, {}", url_count, url_file)

    with open(output_file, 'w') as f_write:
        with open(raw_file, 'r') as f_read:
            # 计行数
            line_count = 0
            # 数值开头
            num_reg = re.compile(r'^[-\d]')  
            # 特殊字符串开头
            param_reg = re.compile(r'^(user_id|group_id|fullname|user_nickname|display_name|user_email|password|rights|login)')

            for line in f_read:
                line_count += 1
                # 将恶意payload部分还原为url
                if line_count > url_count:
                    if line_count == (url_count + 1):
                        logger.debug("Abnormal sample begin here: {}", line_count)
                    if re.search(num_reg, line):
                        line = 'test?id=' + line
                    elif re.search(param_reg, line):
                        line = 'test?params=' + line
                    else:
                        line = 'test?user=' + line
                else:
                    line = url_list[line_count - 1]
                
                f_write.write(line)
                


if __name__ == '__main__':
    # web_app
    dataset = '../../dataset/comparative_eprm/web_app/test_set.txt'
    output = '../../dataset/comparative_eprm/web_app/test_set_with_path.txt'
    # wordpress
    dataset = '../../dataset/comparative_eprm/wordpress/test_set.txt'
    output = '../../dataset/comparative_eprm/wordpress/test_set_with_path.txt'
    url_file = '../../dataset/comparative_eprm/wordpress/normal_url.txt'
    
    # restore_url(dataset, output)
    restore_wordpress_test_set(url_file, dataset, output)