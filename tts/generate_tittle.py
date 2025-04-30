import json
import os
import requests
from pathlib import Path

def generate_intro(json_path, output_dir):
    # 读取JSON文件
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 生成开场白
    intro = f"大家好，这里是今日话题牛，今天为大家带来的内容是：{data['title']}，看看大家的看法是什么样的吧！"
    
    # 生成语音
    url = "http://localhost:8089/v1/tts"
    data = {
        "text": intro,
        "streaming": False,
        "format": "wav"
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成输出文件名
        output_file = os.path.join(output_dir, f"{os.path.basename(json_path).split('.')[0]}_intro.wav")
        
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"开场白语音已保存为 {output_file}")
    else:
        print("请求失败，状态码：", response.status_code)
        print("返回内容：", response.text)

def main():
    # 设置路径
    article_dir = "G:/cc/demo/zhihu/article"
    output_dir = "G:/cc/demo/tts/voice"
    
    # 获取所有JSON文件
    json_files = [f for f in os.listdir(article_dir) if f.endswith('.json')]
    
    if not json_files:
        print("未找到JSON文件")
        return
    
    # 处理第一个文件
    json_file = json_files[-1]  # 使用第二个文件
    json_path = os.path.join(article_dir, json_file)
    
    # 生成开场白
    generate_intro(json_path, output_dir)

if __name__ == "__main__":
    main()
