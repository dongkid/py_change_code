import re
import sys

def convert_php_dict(input_path, output_path):
    """
    将PHP字典文件转换为Python常量格式
    :param input_path: 输入文件路径
    :param output_path: 输出文件路径
    """
    simple_chars = []
    tradition_chars = []
    pattern = re.compile(r"\s*'([^']*)' => '([^']*)',")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = pattern.match(line)
            if match:
                simple_chars.append(match.group(2))
                tradition_chars.append(match.group(1))
    
    # 将字符列表连接为字符串
    simple_str = ''.join(simple_chars)
    tradition_str = ''.join(tradition_chars)
    
    # 写入输出文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f'SIMPLE = "{simple_str}"\n')
        f.write(f'TRADITION = "{tradition_str}"\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_dict.py <input_file> <output_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_php_dict(input_file, output_file)