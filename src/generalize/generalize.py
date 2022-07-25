import re
import subprocess

from keywords import KEYWORDS
from functions import FUNCTIONS
from non_preserved import NON_PREVERSED


class generalizer:
    def __init__(self):
        regex_backslash_quotation = re.compile(r"\\'")          # 单引号包裹的字符串，其间反斜杠+单引号
        regex_single = re.compile(r'\'[^\']*\'')                # 单引号包裹的字符串，其间不含单引号
        regex_double = re.compile(r'"[^"]*"')                   # 双引号包裹的字符串，其间不含双引号
        regex_num = re.compile(r'\b\d+\.?\d*\b')                # 左右都是单词边界的整数或小数
        regex_hex = re.compile(r'0x[a-zA-Z0-9]*')               # 十六进制
        
        self.regex_comment_dash = re.compile(r'-- .*')          # MySQL注释
        self.regex_comment_well_number = re.compile(r'#.*')     # MySQL注释
        
        self.reg_exp_maps = {
            regex_backslash_quotation: 'BSQ',
            regex_single: 'TK_STR',
            regex_double: 'TK_STR',
            regex_num: '0',
            regex_hex: '0',
        }
        # 分隔符
        self.separators = [
            ':=',          # 赋值号
            '\.',          # .
            '\s',          # 空格
            ',',           # 逗号
            '\(',          # 左括号
            '\)',          # 右括号
            '=',           # 等号
            '>',           # >
            '<',           # <
            '\+',          # +
            '/',           # /
            '%',           # %
            '&',           # &
            '\|',          # |
            '\^',          # ^
            '~',           # ~
            '#',           # 井号
            ';',           # 分号
            '\*',          # 星号
            '\-',          # 减号 或 负号
            '!',           # not
            '~',           # 按位取反
        ]
        # 过滤列表：空字符、泛化后的片段、单引号、双引号
        self.filter_list = ['', '0', 'TK_STR', 'TK_IDTF', 'TK_F', 'TK_VAR', '\'', '"']

    
    def add_separator(self, sep):
        self.separators.append(sep)


    # separate strings based on self.separators
    def split(self, raw_str):
        pattern = r'' + '|'.join(self.separators)
        segments = re.split(pattern, raw_str)

        return segments
   

    # step 1 - generalize column/table name to TK_IDTF
    def col_table_generalize(self, raw_file, out_file, col_table_extracted_file):
        regex_list = [r'\w+TK_IDTF\w+', r'\w+\.TK_IDTF']
        count = 0

        with open(out_file, 'w', encoding='gb18030') as f_out:
            with open(col_table_extracted_file, 'r') as f_col_table:
                with open(raw_file, 'r', encoding='gb18030', errors='ignore') as f_raw:

                    for line in f_raw:
                        count += 1
                        col_table_list = f_col_table.readline().strip().split(' ')
                        
                        if col_table_list != []:
                            # duplicate removal
                            col_table_set_list = list(set(col_table_list))
                            # Descending sort based on string length
                            col_table_sorted_list = sorted(col_table_set_list, key = lambda i:len(i), reverse=True)
                            
                            # column/table name -> TK_IDTF
                            for item in col_table_sorted_list:
                                if item != '':
                                    regex = '`{}`'.format(item) + r"|\b" + item + r"\b"
                                    line = re.sub(regex, 'TK_IDTF', line)

                            # Further processing: [TK_TK_IDTFTF] [TK_IDTF.*] [xxx.TK_IDTF]
                            for regex in regex_list:
                                line = re.sub(regex, 'TK_IDTF', line)

                        f_out.write(line)
    
    
    # step 2 - generalize digit -> 0；generalize str -> TK_STR;
    def num_str_generalize(self, string):
        for regex, sub_str in self.reg_exp_maps.items():
            string = re.sub(regex, sub_str, string)
        
        return string
    

    # step 3 - generalize function -> TK_F
    def func_generalize(self, string): 
        func_list = []

        # separate strings
        segments_list = self.split(string)
        
        # filter '', generalized segments and keywords with version number
        for seg in segments_list:
            if seg in self.filter_list:  
                continue
            if seg.upper() in FUNCTIONS:
                func_list.append(seg)
        # duplication removal
        func_set_list = list(set(func_list))

        # function -> TK_F
        # keywords, preserved words and function names overlap, 
        # so that generate [function(] -> [TK_F(], [function*/] -> [TK_F*/]
        for item in func_set_list:
            regex1 = r"\b" + item + r"\("
            regex2 = r"\b" + item + r"\*/"
            string = re.sub(regex1, 'TK_F(', string)
            string = re.sub(regex2, 'TK_F*/', string)
        
        return string

    
    # step 4 - generate variables(system variable and customer variable) -> TK_VAR, alias -> TK_IDTF
    def val_alias_generalize(self, string):
        alias_list = []
        version_keyword_regex = r'^\d+\w+' # [digitxxx]
        
        # generate variable
        string = re.sub(r'@{1,2}\w+', 'TK_VAR', string)

        # separate strings, and filter '', generalized segments, keywords, non-preserved words, ', ", and *
        segments_list = self.split(string)

        for seg in segments_list:
            upper_seg = seg.upper()
            # filter: '', generalized segments, ', "
            if seg in self.filter_list: 
                continue
            # filter: keywords with version number
            if re.search(version_keyword_regex, seg):
                tmp = re.split(r'\d+', upper_seg)[1]
                if tmp in KEYWORDS:
                    continue
            # filter: keywords and noe-preserved words
            if (upper_seg not in KEYWORDS) and (upper_seg not in NON_PREVERSED):
                alias_list.append(seg)
        
        # duplication removal
        alias_set_list = list(set(alias_list))
        
        # generalize alias
        for alias in alias_set_list:
            if re.search(r'^`.*`$', alias): # 切割的片段是被反引号包裹的片段，直接泛化
                alias_regex = alias
            else:
                alias_regex = r"\b" + alias + r"\b"
            string = re.sub(alias_regex, 'TK_IDTF', string)
        
        return string


    # step 5 - generalize comments
    def comment_generalize(self, string):
        string = re.sub(self.regex_comment_dash, '-- TK_C', string)
        string = re.sub(self.regex_comment_well_number, '#TK_C', string)
        
        return string


    # (1) generalize digits and str
    # (2) generalize funciton
    # (3) separate strings and generalize variables and alias
    def generalize(self, raw_file, out_file):
        count = 0 # line number
        with open(out_file, 'w', encoding='gb18030') as f_out:
            with open(raw_file, 'r', encoding='gb18030', errors='ignore') as f_raw:
                for line in f_raw:
                    count += 1
                    print(count)
                    line = self.num_str_generalize(line)    # generalize digits and string
                    line = self.func_generalize(line)       # generalize function
                    line = self.val_alias_generalize(line)  # generalize variables and alias
                    line = self.comment_generalize(line)    # generalize comments
                    f_out.write(line)


# generalize the sql of self-built web app
def generalize_web_app(index, output_path):
    raw_path = '../../dataset/sql/'
    if output_path == '':
        out_path = '../../dataset/generalizer/generalized_dataset/web_app/'
    else:
        out_path = output_path
    file_list = [
        [raw_path+'time_blind_11-28.txt', out_path+'time_blind_col_tab.txt', out_path+'time_blind_col_tab_gen.txt', out_path+'time_blind.txt'], # time_blind
        [raw_path+'bool_blind_11-29.txt', out_path+'bool_blind_col_tab.txt', out_path+'bool_blind_col_tab_gen.txt', out_path+'bool_blind.txt'], # bool_blind
        [raw_path+'illegal_11-30.txt', out_path+'illegal_col_tab.txt', out_path+'illegal_col_tab_gen.txt', out_path+'illegal.txt'], # illegal
        [raw_path+'tautology_12-02.txt', out_path+'tautology_col_tab.txt', out_path+'tautology_col_tab_gen.txt', out_path+'tautology.txt'], # tautology
        [raw_path+'union_12-07.txt', out_path+'union_col_tab.txt', out_path+'union_col_tab_gen.txt', out_path+'union.txt'], # union
        [raw_path+'normal_1-18.txt', out_path+'normal_col_tab.txt', out_path+'normal_col_tab_gen.txt', out_path+'normal.txt'], # normal
    ]

    # dataset
    sql_file = file_list[index][0]
    # column/table name file
    col_table_extracted_file = file_list[index][1]
    # generalized column/table name file
    col_table_genaralized_file = file_list[index][2]
    # result file
    result_file = file_list[index][3]

    # win
    # call_list = ['./colx/colx.exe', sql_file, col_table_extracted_file]
    # linux
    call_list = ['./colx/colx', sql_file, col_table_extracted_file]

    # call parser to extract column/table name
    call_stat = subprocess.call(call_list, shell=False)
    if call_stat == 0:
        print("shell 命令执行成功")
    else:
        print("shell 命令执行异常")
    
    # parse and generalize
    generalizer_instance = generalizer()
    generalizer_instance.col_table_generalize(sql_file, col_table_genaralized_file, col_table_extracted_file) 
    generalizer_instance.generalize(col_table_genaralized_file, result_file)


# generalize sql of wordpress
def generalize_wordpress(index, output_path):
    raw_path = '../../dataset/sql/wordpress/'
    if output_path == '':
        out_path = '../../dataset/generalizer/generalized_dataset/wordpress/'
    else:
        out_path = output_path
    class_list = ['time_blind_wp', 'bool_blind_wp', 'illegal_wp', 'tautology_wp', 'union_wp', 'normal_wp']
    file_list = []
    
    # 0-time_blind， 1-bool_blind， 2-illegal，3-tautology，4-union, 5-normal
    for i in range(0,6):
        raw_file = raw_path + class_list[i] + '.txt'
        f_col_tab = out_path + class_list[i] + '_col_tab.txt'
        f_col_tab_gen = out_path + class_list[i] + '_col_tab_gen.txt'
        f_result = out_path + class_list[i] + '.txt'
        file_list.append([raw_file, f_col_tab, f_col_tab_gen, f_result])

    # dataset
    sql_file = file_list[index][0]
    # column/table name file
    col_table_extracted_file = file_list[index][1]
    # generalized column/table name file
    col_table_genaralized_file = file_list[index][2]
    # result file
    result_file = file_list[index][3]

    # win
    # call_list = ['./colx/colx.exe', sql_file, col_table_extracted_file]
    # Linux
    call_list = ['./colx/colx', sql_file, col_table_extracted_file]

    # call parser to extract column/table name
    call_stat = subprocess.call(call_list, shell=False)
    if call_stat == 0:
        print("shell 命令执行成功")
    else:
        print("shell 命令执行异常")
    
    # parse and generalize
    generalizer_instance = generalizer()
    generalizer_instance.col_table_generalize(sql_file, col_table_genaralized_file, col_table_extracted_file)
    generalizer_instance.generalize(col_table_genaralized_file, result_file)




if __name__ == '__main__':
    # 0-time_blind， 1-bool_blind， 2-illegal，3-tautology，4-union, 5-normal

    generalize_web_app(5, '')