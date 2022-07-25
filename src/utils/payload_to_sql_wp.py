import re
import random
from tqdm import tqdm

from template_wp_map import TEMPLATE_WP_MAP


# determin the start char of payload, and return the type corresponding to TEMPLATE_WP_MAP
def start_char(type, payload):
    # [')))]
    if re.search(r"^'\)\)\)", payload):
        return 'single_quote_3_parenthesis'
    # ['))]
    elif re.search(r"^'\)\)", payload):
        return 'single_quote_2_parenthesis'
    # [')]
    elif re.search(r"^'\)", payload):
        return 'sindle_quote_1_parenthesis'
    # [']
    elif re.search(r"^'", payload):
        return 'single_quote'
    # [))]
    elif re.search(r"^\)\)", payload):
        return 'num_2_parenthesis'
    # [)]
    elif re.search(r"^\)", payload):
        return 'num_1_parenthesis'
    # [ ] [;] [/*]
    elif re.search(r"^(\s|;|/\*)", payload):
        if type == 'comment':
            return 'num&num_tail'
        else:
            return 'num_tail'
    else:
        return 'others'


# inject payload into template of wordpress normal sql
def inject(payload_comment_file, payload_no_comment_file, out_file):
    with open(out_file, 'w') as f_write:
        # get payload contains comment
        with open(payload_comment_file, 'r') as f_c_read:
            count = 0       # line number

            for line in tqdm(f_c_read):
                count += 1
                map_key = start_char('commit', line)

                if map_key == 'others':
                    print("[C]-[{}]".format(count))
                    continue
                elif map_key == 'num&num_tail':
                    rand_key = random.choice(['num', 'num_tail'])
                    index = random.randint(0, len(TEMPLATE_WP_MAP[rand_key]) - 1)
                    template_wp = TEMPLATE_WP_MAP[rand_key][index]
                else:
                    index = random.randint(0, len(TEMPLATE_WP_MAP[map_key]) - 1)
                    template_wp = TEMPLATE_WP_MAP[map_key][index]

                sql = "{}{}{}\n".format(template_wp[0], line.rstrip('\n'), template_wp[1])
                # sql = template_wp[0] + line.rstrip('\n') + template_wp[1] + '\n'
                f_write.write(sql)
        
        # get payload has no comment
        with open(payload_no_comment_file, 'r') as f_n_read:
            count = 0       # line number

            for line in tqdm(f_n_read):
                count += 1
                map_key = start_char('no_commit', line)

                if map_key == 'others':
                    print("[N]-[{}]".format(count))
                    continue
                else:
                    index = random.randint(0, len(TEMPLATE_WP_MAP[map_key]) - 1)
                    template_wp = TEMPLATE_WP_MAP[map_key][index]

                sql = "{}{}{}\n".format(template_wp[0], line.rstrip('\n'), template_wp[1])
                # sql = template_wp[0] + line.rstrip('\n') + template_wp[1] + '\n'
                f_write.write(sql)


if __name__ == "__main__":
    payload_path = '../../dataset/payload/wordpress/'
    out_path = '../../dataset/sql/wordpress/'
    class_list = ['time_blind', 'bool_blind', 'illegal', 'tautology', 'union']
    
    payload_comment_file = [payload_path + item + '_comment.txt' for item in class_list]
    payload_no_comment_file = [payload_path + item + '_no_comment.txt' for item in class_list]
    out_file = [out_path + item + '_wp.txt' for item in class_list]

    # 0-time_blind, 1-bool_blind, 2-illegal, 3-tautology, 4-union
    for index in range(0,5):
        inject(payload_comment_file[index], payload_no_comment_file[index], out_file[index])