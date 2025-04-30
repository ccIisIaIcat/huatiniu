import json
import os
import requests
from pathlib import Path

OPENAI_API_KEY="sk-iovSklr9Q3aW95E3gwtCoMMxLDCE61gNhWq71JwFSJKyaJ9b"
OPENAI_API_MAX_TOKENS=4000
OPENAI_API_TEMPERATURE=0.7

class OpenAIAPI:
    def __init__(self, api_key: str):
        """初始化OpenAI API客户端
        
        Args:
            api_key: OpenAI API密钥
        """
        self.api_key = api_key
        self.base_url = "https://api.openai-proxy.org/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def chat(self, user_message: str, system_message: str = "You are a helpful assistant.") -> dict:
        """发送聊天请求
        
        Args:
            user_message: 用户消息
            system_message: 系统消息，用于设置AI助手的行为
            
        Returns:
            API响应的JSON数据
        """
        payload = {
            "model": "gpt-4o-2024-11-20",
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"API请求失败: {e}")
            return {"error": str(e)}

def check_content(content):
    # 初始化OpenAI API客户端
    api = OpenAIAPI("sk-iovSklr9Q3aW95E3gwtCoMMxLDCE61gNhWq71JwFSJKyaJ9b")
    
    # 构建提示词
    prompt = f"""
    请判断以下内容是否适合做成视频稿，返回严格的JSON格式，不要包含任何其他文字或标记。
    判断标准：
    1. 如果包含较多英文内容，包括文献，论文，书籍等，则返回false
    2、其他的只要表达还算清晰，都可以返回true
    内容：
    {content}
    
    请返回如下格式的JSON(重要！！！不要包含```json```等类似的形式，我需要直接解析你的返回值)：
    {{
        "suitable": true/false,
        "reason": "判断理由"
    }}
    """
    
    # 调用API
    response = api.chat(prompt, "你是一个专业的视频内容评估专家")
    if "error" in response:
        print(f"API调用失败: {response['error']}")
        return None
    
    # 解析返回的JSON
    try:
        print(response['choices'][0]['message']['content'])
        result = json.loads(response['choices'][0]['message']['content'])
        return result['suitable']
    except:
        print("解析返回结果失败")
        return None

def process_article(json_path, output_dir):
    # 读取JSON文件
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 检查每个content
    results = []
    for section in data['content']:
        # 将整个section的内容合并为一个字符串
        content = '\n'.join(section)
        is_suitable = check_content(content)
        if is_suitable is None:
            results.append(False)
        else:
            results.append(is_suitable)
    
    # 生成输出文件名
    output_file = os.path.join(output_dir, os.path.basename(json_path))
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # 保存结果
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"检查结果已保存为: {output_file}")

def main():
    # 设置路径
    article_dir = "G:/cc/demo/zhihu/article"
    output_dir = "G:/cc/demo/check/check"
    
    # 获取所有JSON文件
    json_files = [f for f in os.listdir(article_dir) if f.endswith('.json')]
    
    if not json_files:
        print("未找到JSON文件")
        return
    
    # 处理第一个文件
    json_file = json_files[-1]  # 使用最后一个文件
    json_path = os.path.join(article_dir, json_file)
    
    # 处理文章
    process_article(json_path, output_dir)

if __name__ == "__main__":
    main()
