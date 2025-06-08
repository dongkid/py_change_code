'''
繁体与简体相互转换：
 '''

from constant import SIMPLE, TRADITION

# 简体转繁体
def toTraditionString(str):
    # 用字符串+比较耗内存与时间
    output_str_list = []
    str_len = len(str)
    for i in range(str_len):
        found_index = SIMPLE.find(str[i])
        if not (found_index == -1):
            output_str_list.append(TRADITION[found_index])
        else:
            output_str_list.append(str[i])
    return   "".join(output_str_list)


# 繁体转简体
def toSimpleString(str):
    # 用字符串+比较耗内存与时间
    output_str_list = []
    str_len = len(str)
    for i in range(str_len):
        found_index = TRADITION.find(str[i])
        if not (found_index == -1):
            output_str_list.append(SIMPLE[found_index])
        else:
            output_str_list.append(str[i])
    return   "".join(output_str_list)