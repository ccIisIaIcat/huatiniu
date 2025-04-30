from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def read_local_html(file_path):
    """读取本地HTML文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_hot_items(html_content):
    """获取所有HotItem-content的内容"""
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 查找所有class为HotItem-content的div
    hot_items = soup.find_all('div', class_='HotItem-content')
    
    # 提取每个热榜项的内容
    items_data = []
    for index, item in enumerate(hot_items, 1):
        try:
            # 查找链接
            link_element = item.find('a')
            link = link_element.get('href') if link_element else "无链接"
            
            items_data.append({
                "序号": index,
                "文本内容": item.get_text(strip=True),
                "链接": link,
                "HTML内容": str(item)
            })
            print(f"已获取第 {index} 个热榜内容")
            print(f"链接: {link}")
            
        except Exception as e:
            print(f"获取第 {index} 个内容时出错: {e}")
            continue
    
    return items_data

def save_items(items_data):
    """保存热榜内容到文件"""
    # 创建保存目录
    save_dir = "知乎热榜数据"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(save_dir, f"热榜内容_{timestamp}.json")
    
    # 保存为JSON文件
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(items_data, f, ensure_ascii=False, indent=2)
    
    print(f"数据已保存到: {filename}")
    return filename

def main():
    try:
        # 读取本地HTML文件
        file_path = r"G:\cc\demo\知乎页面源码\知乎热榜_20250428_125230.html"
        print("正在读取本地HTML文件...")
        html_content = read_local_html(file_path)
        
        # 获取热榜内容
        print("正在解析热榜内容...")
        items_data = get_hot_items(html_content)
        
        # 保存数据
        if items_data:
            saved_file = save_items(items_data)
            print(f"共获取到 {len(items_data)} 个热榜内容")
        else:
            print("未获取到热榜内容")
        
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
