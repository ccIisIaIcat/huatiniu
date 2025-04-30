import requests
import json

OPENAI_API_KEY="closeAI 密钥"
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

# def main():
#     # 创建API客户端
#     client = OpenAIAPI(OPENAI_API_KEY)
    
#     # 发送测试消息
#     response = client.chat("你好！")
    
#     # 打印完整响应
#     print("API完整响应:")
#     print(json.dumps(response, ensure_ascii=False, indent=2))
    
#     # 如果响应成功，打印AI的回复
#     if "choices" in response:
#         ai_reply = response["choices"][0]["message"]["content"]
#         print("\nAI回复:")
#         print(ai_reply)
