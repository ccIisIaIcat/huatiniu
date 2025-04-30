import requests

url = "http://localhost:8089/v1/tts"
data = {
    "text": "你好，世界！这是一个测试语音合成的请求。",
    "streaming": False,
    "format": "wav"
}

response = requests.post(url, json=data)

if response.status_code == 200:
    with open("output.wav", "wb") as f:
        f.write(response.content)
    print("语音已保存为 output.wav")
else:
    print("请求失败，状态码：", response.status_code)
    print("返回内容：", response.text)