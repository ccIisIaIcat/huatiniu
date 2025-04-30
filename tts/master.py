import json
import os
import requests
from pathlib import Path
import re
from generate_tittle import generate_intro
from generate_content import process_article, generate_voice
from generate_end import generate_outro

def main():
    # 设置路径
    article_dir = "G:/cc/demo/zhihu/article"
    check_dir = "G:/cc/demo/check/check"
    output_dir = "G:/cc/demo/tts/voice"
    
    # 获取用户输入的JSON文件名
    json_files = [f for f in os.listdir(article_dir) if f.endswith('.json')]
    if not json_files:
        raise FileNotFoundError("未找到任何json文件")
    json_files.sort()
    json_name = json_files[-1]
    
    # 构建完整路径
    article_path = os.path.join(article_dir, json_name)
    check_path = os.path.join(check_dir, json_name)
    
    # 检查文件是否存在
    if not os.path.exists(article_path):
        print(f"错误：在 {article_dir} 中找不到文件 {json_name}")
        return
    
    if not os.path.exists(check_path):
        print(f"错误：在 {check_dir} 中找不到文件 {json_name}")
        return
    
    # 读取检查结果
    with open(check_path, 'r', encoding='utf-8') as f:
        check_results = json.load(f)
    
    # 生成开场白
    print("\n生成开场白...")
    generate_intro(article_path, output_dir)
    
    # 处理文章内容
    print("\n处理文章内容...")
    processed_sections = process_article(article_path)
    
    # 根据检查结果生成语音
    for section_num, text in processed_sections:
        if check_results[section_num]:  # 如果检查结果为True
            print(f"\n处理第 {section_num + 1} 部分：")
            print(text)
            
            # 生成输出文件名（包含序列号）
            output_file = os.path.join(output_dir, f"{os.path.splitext(json_name)[0]}_part{section_num + 1}.wav")
            
            # 生成语音
            generate_voice(text, output_file)
        else:
            print(f"\n跳过第 {section_num + 1} 部分（不适合生成视频稿）")
    
    # 生成结尾语音
    print("\n生成结尾语音...")
    generate_outro(article_path, output_dir)
    
    print("\n处理完成！")

if __name__ == "__main__":
    main()
