from bs4 import BeautifulSoup
import json

def get_text_from_element(element):
    """递归获取元素中的所有文本内容"""
    if element.name == 'li':  # 如果是列表项，作为单独的文本
        return [element.get_text(strip=True)]
    
    texts = []
    for child in element.children:
        if child.name == 'li':  # 列表项
            text = child.get_text(strip=True)
            if text:
                texts.append(text)
        elif child.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote']:  # 块级元素
            text = child.get_text(strip=True)
            if text:
                texts.append(text)
        elif child.string and child.string.strip():  # 直接文本
            texts.append(child.string.strip())
        elif hasattr(child, 'children'):  # 其他可能包含子元素的元素
            texts.extend(get_text_from_element(child))
    
    return texts

def parse_answer(html_file):
    """解析知乎回答HTML文件，返回作者和文本列表
    
    Args:
        html_file: HTML文件路径
        
    Returns:
        tuple: (作者名称, 文本列表)，如果解析失败返回 (None, [])
    """
    try:
        # 读取HTML文件
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找第一个class为"ContentItem AnswerItem"的div
        answer_div = soup.find('div', class_=['ContentItem', 'AnswerItem'])
        
        if not answer_div:
            return None, []
        
        # 获取作者名称
        data_zop = answer_div.get('data-zop', '{}')
        data_dict = json.loads(data_zop)
        author_name = data_dict.get('authorName', None)
        
        # 获取回答内容
        content_element = answer_div.find(attrs={'itemprop': 'text'})
        if not content_element:
            return author_name, []
        
        # 获取所有文本内容并过滤空字符串
        content_list = [text for text in get_text_from_element(content_element) if text]
        
        return author_name, content_list
        
    except Exception as e:
        print(f"解析出错: {e}")
        return None, []

# if __name__ == "__main__":
#     html_file = r"G:\cc\demo\知乎回答HTML\回答_1_20250428_142441.html"
#     author, texts = parse_answer(html_file)
    
#     print(f"\n作者：{author}")
#     print(f"\n找到 {len(texts)} 段文本：")
#     for i, text in enumerate(texts, 1):
#         print(f"\n第 {i} 段：{text[:100]}..." if len(text) > 100 else f"\n第 {i} 段：{text}")
