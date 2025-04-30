import json
import os
import requests
from pathlib import Path

def generate_outro(json_path, output_dir):
    # 读取JSON文件
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 生成结尾语
    outro = f"以上就是关于{data['title']}的全部内容，如果觉得内容不错的话，欢迎点赞关注，我们下期再见！"
    
    # 生成语音
    url = "http://localhost:8089/v1/tts"
    data = {
        "text": outro,
        "streaming": False,
        "format": "wav"
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成输出文件名
        output_file = os.path.join(output_dir, f"{os.path.basename(json_path).split('.')[0]}_outro.wav")
        
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"结尾语音已保存为 {output_file}")
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
    
    # 处理最新的文件
    json_file = json_files[-1]
    json_path = os.path.join(article_dir, json_file)
    
    # 生成结尾语音
    generate_outro(json_path, output_dir)

if __name__ == "__main__":
    main()

