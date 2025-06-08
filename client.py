'''
简体与繁体相互转换的客户端入口文件。
'''

import os
import re
import chardet
import argparse
import sys
from changeCode import toTraditionString, toSimpleString

def read_text_from_file(file_path):
    """从指定路径读取文本文件内容。"""
    if not os.path.exists(file_path):
        print(f'文件 {file_path} 不存在')
        return None
    
    with open(file_path, 'rb') as file:
        content_bytes = file.read()
    
    # 使用chardet检测编码
    result = chardet.detect(content_bytes)
    encoding = result['encoding']
    confidence = result['confidence']
    
    try:
        # 根据检测结果尝试解码
        return content_bytes.decode(encoding)
    except (UnicodeDecodeError, TypeError):
        # 定义备选编码列表（按优先级排序）
        fallback_encodings = ['GB18030', 'GBK', 'Big5', 'utf-8']
        
        # 尝试所有备选编码
        for enc in fallback_encodings:
            try:
                return content_bytes.decode(enc)
            except (UnicodeDecodeError, TypeError):
                continue
        
        # 所有编码都失败时使用utf-8忽略错误模式
        print('所有编码尝试失败，使用utf-8忽略错误模式')
        return content_bytes.decode('utf-8', errors='ignore')

def write_text_to_file(file_path, content):
    """将内容写入到指定路径的文本文件中。"""
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='简体繁体转换工具')
    parser.add_argument('-i', '--input', help='输入文件或目录路径')
    parser.add_argument('-t', '--type', choices=['1', '2'], help='转换类型: 1-简体转繁体, 2-繁体转简体')
    parser.add_argument('-o', '--output', help='输出文件或目录路径')
    args = parser.parse_args()
    
    # 无参数时使用默认设置
    if not any(vars(args).values()):
        input_path = './input'
        conversion_type = '2'
        output_path = './output'
        interactive = False
    else:
        # 检查必需参数
        if not args.input or not args.type or not args.output:
            print('错误：必须同时提供输入路径、转换类型和输出路径')
            parser.print_help()
            return
            
        input_path = args.input
        conversion_type = args.type
        output_path = args.output
        interactive = True if not all([args.input, args.type, args.output]) else False
    
    # 如果有缺失参数，进入交互模式
    if interactive:
        if not args.input:
            input_path = input('请输入输入文本文件的路径: ')
        if not args.type:
            conversion_type = input('请选择转换类型 (1. 简体转繁体 2. 繁体转简体): ')
        if not args.output:
            output_path = input('请输入输出文件的路径: ')
    
    if os.path.isdir(input_path):
        # 非交互模式下确保输出目录存在
        if not interactive:
            if not os.path.exists(output_path):
                os.makedirs(output_path)
                
        txt_files = [f for f in os.listdir(input_path) if f.endswith('.txt')]
        for txt_file in txt_files:
            input_file = os.path.join(input_path, txt_file)
            text = read_text_from_file(input_file)
            if text is None:
                continue
                
            # 执行文本转换
            if conversion_type == '1':
                converted_text = toTraditionString(text)
            elif conversion_type == '2':
                converted_text = toSimpleString(text)
            else:
                print('无效的转换类型')
                return
                
            # 处理输出路径
            if os.path.isdir(output_path):
                base_name = os.path.basename(txt_file)
                output_file = os.path.join(output_path, base_name)
            else:
                output_file = output_path
                
            # 非交互模式下直接覆盖
            if not interactive:
                write_text_to_file(output_file, converted_text)
            else:
                # 交互模式下检查文件是否存在
                if os.path.exists(output_file):
                    choice = input(f'文件 {output_file} 已存在，是否替换？(y/n): ')
                    if choice.lower() != 'y':
                        # 自动生成新文件名
                        file_dir = os.path.dirname(output_file)
                        file_name = os.path.basename(output_file)
                        name, ext = os.path.splitext(file_name)
                        counter = 1
                        while os.path.exists(os.path.join(file_dir, f"{name}_{counter}{ext}")):
                            counter += 1
                        new_output_file = os.path.join(file_dir, f"{name}_{counter}{ext}")
                        write_text_to_file(new_output_file, converted_text)
                        print(f'文件已保存为 {new_output_file}')
                    else:
                        write_text_to_file(output_file, converted_text)
                else:
                    write_text_to_file(output_file, converted_text)
        
        print('目录内所有文件转换完成')
    else:
        text = read_text_from_file(input_path)
        if text is None:
            return
            
        # 执行文本转换
        if conversion_type == '1':
            converted_text = toTraditionString(text)
        elif conversion_type == '2':
            converted_text = toSimpleString(text)
        else:
            print('无效的转换类型')
            return
            
        # 处理输出路径
        if os.path.isdir(output_path):
            base_name = os.path.basename(input_path)
            output_file = os.path.join(output_path, base_name)
        else:
            output_file = output_path
            
        # 非交互模式下直接覆盖
        if not interactive:
            # 确保输出目录存在
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            write_text_to_file(output_file, converted_text)
            print('转换完成')
        else:
            # 交互模式下检查文件是否存在
            if os.path.exists(output_file):
                choice = input(f'文件 {output_file} 已存在，是否替换？(y/n): ')
                if choice.lower() != 'y':
                    # 自动生成新文件名
                    file_dir = os.path.dirname(output_file)
                    file_name = os.path.basename(output_file)
                    name, ext = os.path.splitext(file_name)
                    counter = 1
                    while os.path.exists(os.path.join(file_dir, f"{name}_{counter}{ext}")):
                        counter += 1
                    new_output_file = os.path.join(file_dir, f"{name}_{counter}{ext}")
                    write_text_to_file(new_output_file, converted_text)
                    print(f'文件已保存为 {new_output_file}')
                else:
                    write_text_to_file(output_file, converted_text)
            else:
                write_text_to_file(output_file, converted_text)
            print('转换完成')

if __name__ == '__main__':
    main()