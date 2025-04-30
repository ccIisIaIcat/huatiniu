import json
import os
import requests
from pathlib import Path
import re

def process_article(json_path):
    # 读取JSON文件
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 处理每个数组的内容
    processed_sections = []
    for i, section in enumerate(data['content']):
        # 处理每个句子，删除除了逗号和句号以外的标点符号
        processed_sentences = []
        for sentence in section:
            # 保留逗号和句号，删除其他标点符号
            processed = re.sub(r'[^\w\s，。]', '', sentence)
            processed_sentences.append(processed)
        
        # 用逗号连接所有句子
        text = '\n'.join(processed_sentences)
        processed_sections.append((i, text))
    
    return processed_sections

def generate_voice(text, output_path):
    url = "http://localhost:8089/v1/tts"
    data = {
        "text": text,
        "streaming": False,
        "format": "wav"
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"语音已保存为 {output_path}")
    else:
        print("请求失败，状态码：", response.status_code)
        print("返回内容：", response.text)

def main():
    # 设置路径
    article_dir = Path("G:/cc/demo/zhihu/article")
    output_dir = Path("G:/cc/demo/tts/voice")
    
    # 获取所有JSON文件
    json_files = list(article_dir.glob("*.json"))
    
    if not json_files:
        print("未找到JSON文件")
        return
    
    # 处理第一个文件
    json_file = json_files[-1]
    processed_sections = process_article(json_file)
    
    # 为每个部分生成语音
    for section_num, text in processed_sections:
        print(f"\n处理第 {section_num + 1} 部分：")
        print(text)
        
        # 生成输出文件名（包含序列号）
        output_file = output_dir / f"{json_file.stem}_part{section_num + 1}.wav"
        
        # 生成语音
        generate_voice(text, str(output_file))

if __name__ == "__main__":
    main() 