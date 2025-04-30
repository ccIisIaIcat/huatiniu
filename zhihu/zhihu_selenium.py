from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
import pickle
import pandas as pd
from datetime import datetime
import os
from ask import OpenAIAPI, OPENAI_API_KEY
import random
from check import parse_answer  # 添加导入

article = {
    "title": "",
    "answers": [],
    "link": "",
    "content":[],
    "author":[],
    "pic_tittle":[],
    "pic_answer":[]
}

def save_cookies(driver, cookie_path='zhihu_cookies.pkl'):
    """保存Cookie到文件"""
    cookies = driver.get_cookies()
    with open(cookie_path, 'wb') as f:
        pickle.dump(cookies, f)
    print("Cookie已保存！")

def load_cookies(driver, cookie_path='zhihu_cookies.pkl'):
    """从文件加载Cookie"""
    try:
        with open(cookie_path, 'rb') as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            driver.add_cookie(cookie)
        print("Cookie加载成功！")
        return True
    except FileNotFoundError:
        print("未找到Cookie文件，需要手动登录")
        return False

def setup_driver():
    """配置并返回Chrome WebDriver"""
    chrome_options = Options()
    # 添加更多的浏览器特征
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # 随机设置一个常见的窗口大小
    window_sizes = ['1920,1080', '1366,768', '1440,900', '1536,864']
    chrome_options.add_argument(f'--window-size={random.choice(window_sizes)}')
    
    # 使用更真实的 User-Agent
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    ]
    chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
    
    # 添加其他必要的参数
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # 修改 webdriver 特征
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        '''
    })
    
    return driver

def manual_login(driver, wait):
    """手动登录并保存Cookie"""
    print("请在30秒内完成扫码登录...")
    try:
        # 等待登录成功（通过检查导航栏上的用户头像）
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "AppHeader-profile"))
        )
        print("登录成功！")
        save_cookies(driver)
        return True
    except Exception as e:
        print("登录超时或失败")
        return False

def analyze_page_structure(driver, wait):
    """分析页面结构"""
    # 等待页面加载完成
    time.sleep(5)  # 给页面足够的加载时间
    
    # 获取页面源码
    page_source = driver.page_source
    
    # 使用BeautifulSoup解析页面
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # 创建保存目录
    save_dir = "知乎页面分析"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 保存完整的页面源码
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_file = os.path.join(save_dir, f"页面源码_{timestamp}.html")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(page_source)
    
    # 打印页面结构
    print("\n=== 页面主要元素分析 ===")
    
    # 查找所有可能的热榜相关元素
    hot_sections = soup.find_all('section')
    print(f"\n找到 {len(hot_sections)} 个section元素")
    
    for idx, section in enumerate(hot_sections, 1):
        print(f"\n--- Section {idx} ---")
        print(f"类名: {section.get('class', '无类名')}")
        print(f"ID: {section.get('id', '无ID')}")
        
        # 查找该section下的标题元素
        titles = section.find_all(['h2', 'div', 'a'])
        print(f"包含 {len(titles)} 个可能的标题元素")
        for title in titles[:3]:  # 只打印前3个作为示例
            print(f"元素: {title.name}")
            print(f"类名: {title.get('class', '无类名')}")
            print(f"文本: {title.get_text().strip()[:50]}...")
    
    print(f"\n页面分析结果已保存到: {html_file}")
    return html_file

def get_hot_titles(driver, wait):
    """获取热榜标题"""
    # 等待热榜内容加载
    wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "HotList-list"))
    )
    
    # 获取所有热榜项
    hot_items = driver.find_elements(By.CLASS_NAME, "HotItem")
    
    titles = []
    for item in hot_items:
        try:
            # 获取标题元素
            title_element = item.find_element(By.CLASS_NAME, "HotItem-title")
            # 获取排名
            index = item.find_element(By.CLASS_NAME, "HotItem-index").text
            # 获取标题文本
            title = title_element.text
            # 获取链接
            link = title_element.find_element(By.TAG_NAME, "a").get_attribute("href")
            # 获取热度
            metrics = item.find_element(By.CLASS_NAME, "HotItem-metrics").text
            
            titles.append({
                "排名": index,
                "标题": title,
                "链接": link,
                "热度": metrics
            })
            print(f"已获取第{index}条：{title}")
        except Exception as e:
            print(f"获取标题时出错: {e}")
            continue
    
    return titles

def save_titles(titles, save_dir="知乎热榜数据"):
    """保存热榜标题到文件"""
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(save_dir, f"热榜标题_{timestamp}.json")
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(titles, f, ensure_ascii=False, indent=2)
    
    print(f"热榜标题已保存到: {filename}")
    return filename

def get_hot_items(driver, wait):
    """获取所有HotItem-content的内容"""
    # 等待热榜内容加载
    wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "HotItem-content"))
    )
    
    # 获取页面源码并解析
    html_content = driver.page_source
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

def save_hot_list(hot_list_data):
    """保存热榜数据到CSV文件"""
    # 创建保存目录
    save_dir = "知乎热榜数据"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 生成文件名，包含时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(save_dir, f"知乎热榜_{timestamp}.csv")
    
    # 转换为DataFrame并保存
    df = pd.DataFrame(hot_list_data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"热榜数据已保存到: {filename}")
    return filename

def random_sleep(min_time=1, max_time=3):
    """随机等待一段时间"""
    time.sleep(random.uniform(min_time, max_time))

def simulate_human_behavior(driver):
    """模拟人类行为"""
    # 随机滚动
    for _ in range(random.randint(2, 4)):
        driver.execute_script(f"window.scrollTo(0, {random.randint(100, 500)});")
        random_sleep(0.5, 1.5)
    
    # 移动到页面顶部
    driver.execute_script("window.scrollTo(0, 0);")
    random_sleep()

def save_article_json(article_data):
    """将article数据保存为JSON文件"""
    # 创建保存目录（使用相对路径）
    save_dir = "article"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 生成文件名，包含时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(save_dir, f"article_{timestamp}.json")
    
    # 保存为JSON文件
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(article_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n文章数据已保存到: {filename}")
    return filename

def get_existing_titles():
    """读取已有的文章标题"""
    existing_titles = []
    article_dir = "article"
    
    if os.path.exists(article_dir):
        for filename in os.listdir(article_dir):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(article_dir, filename), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if data.get('title'):
                            existing_titles.append(data['title'])
                except Exception as e:
                    print(f"读取文件 {filename} 时出错: {e}")
    
    return existing_titles

def take_screenshot(driver, prefix, save_dir="pic"):
    """保存页面截图
    Args:
        driver: WebDriver实例
        prefix: 图片文件名前缀
        save_dir: 保存目录
    Returns:
        str: 保存的图片文件名
    """
    # 创建保存目录
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 生成带时间戳的文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{prefix}_{timestamp}.png"
    filepath = os.path.join(save_dir, filename)
    
    try:
        # 等待页面加载完成
        time.sleep(2)
        # 获取页面高度并设置窗口大小
        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1920, total_height)
        # 截图
        driver.save_screenshot(filepath)
        print(f"截图已保存: {filepath}")
        return filename
    except Exception as e:
        print(f"截图失败: {e}")
        return None

def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 30)
    
    try:
        # 先访问知乎首页
        print("正在访问知乎首页...")
        driver.get("https://www.zhihu.com")
        random_sleep(2, 4)

        # 尝试加载Cookie
        if not load_cookies(driver):
            # Cookie加载失败，需要手动登录
            print("需要手动登录一次以保存Cookie...")
            if not manual_login(driver, wait):
                print("登录失败，程序退出")
                return

        # 刷新页面，使Cookie生效
        driver.refresh()
        random_sleep(2, 4)
        
        # 模拟人类行为
        simulate_human_behavior(driver)

        # 访问热榜
        print("正在访问知乎热榜...")
        driver.get("https://www.zhihu.com/hot")
        random_sleep(2, 4)
        simulate_human_behavior(driver)
        
        # 获取热榜内容
        print("正在获取热榜内容...")
        items_data = get_hot_items(driver, wait)
        
        # 保存数据
        if items_data:
            saved_file = save_items(items_data)
            print(f"共获取到 {len(items_data)} 个热榜内容")
            
            # 转换数据为键值对格式
            news_dict = {}
            for item in items_data:
                news_dict[str(item['序号'])] = {
                    'title': item['文本内容'],
                    'link': item['链接']
                }
            
            print("\n转换后的数据格式：")
            print(json.dumps(news_dict, ensure_ascii=False, indent=2))
            
            # 获取已有的文章标题
            existing_titles = get_existing_titles()
            print(f"\n已收录的文章数量：{len(existing_titles)}")
            
            # 构造提示词并调用OpenAI API
            prompt = """请从以下知乎热榜话题中选择一个最有趣的话题。

            评判标准：
            1. 话题的有意思程度
            2. 话题的受众
            3. 话题最好是一些形而上的大话题
            4. 必须选择一个未被收录的话题

            已收录的话题（请不要选择这些或相关的主题）：
            """
            
            # 添加已收录的话题列表
            for title in existing_titles:
                prompt += f"\n- {title}"
            
            prompt += "\n\n请以JSON格式返回，格式要求（重要！不能包含```json{}```等注释字样）：\n"
            prompt += """
            {
                "id": "选中话题的序号",
                "title": "精简后的核心标题，必须是疑问句，需要把问题描述清楚，让读者知道问题背景。"
            }

            以下是当前热榜话题列表：
            """
            
            # 添加当前热榜话题列表
            for idx, item in news_dict.items():
                prompt += f"\n{idx}. {item['title']}"
            
            # 调用OpenAI API
            client = OpenAIAPI(OPENAI_API_KEY)
            response = client.chat(prompt)
            
            if "choices" in response:
                result = response["choices"][0]["message"]["content"]
                print("\nAI选择的最佳话题：")
                print(result)
                
                # 解析AI返回的JSON结果
                try:
                    selected = json.loads(result)
                    selected_id = selected["id"]
                    
                    # 填充article字典
                    article["title"] = selected["title"]
                    article["link"] = news_dict[selected_id]["link"]
                    
                    print("\n准备打开链接：", article["link"])
                    
                    # 在访问文章链接前先进行一些随机操作
                    random_sleep(2, 4)
                    simulate_human_behavior(driver)
                    
                    # 打开选中的文章链接
                    driver.get(article["link"])
                    print("已打开文章页面")
                    
                    # 等待并模拟人类行为
                    random_sleep(3, 5)
                    simulate_human_behavior(driver)
                    
                    # 尝试获取问题标题，验证页面是否正常加载
                    try:
                        title_element = wait.until(
                            EC.presence_of_element_located((By.CLASS_NAME, "QuestionHeader-title"))
                        )
                        print("\n成功加载问题：", title_element.text)
                        
                        # 对问题页面进行截图
                        screenshot_filename = take_screenshot(driver, "question")
                        if screenshot_filename:
                            article["pic_tittle"].append(screenshot_filename)
                        
                        # 等待页面完全加载
                        random_sleep(2, 3)
                        simulate_human_behavior(driver)
                        
                        # 获取页面源码并解析
                        page_source = driver.page_source
                        soup = BeautifulSoup(page_source, 'html.parser')
                        
                        # 查找所有带有itemprop="url"的meta标签
                        meta_tags = soup.find_all('meta', attrs={'itemprop': 'url'})
                        answer_urls = []
                        
                        # 筛选出包含"answer"的URL
                        for meta in meta_tags:
                            url = meta.get('content', '')
                            if url and 'answer' in url:
                                answer_urls.append(url)
                        
                        print("\n找到的回答URL：")
                        # 只打印前20个回答URL
                        for i, url in enumerate(answer_urls[:20], 1):
                            print(f"{i}. {url}")
                        
                        print(f"\n共找到 {len(answer_urls)} 个有效回答URL")
                        
                        # 将回答URL保存到article字典中
                        article["answers"] = answer_urls
                        
                        # 创建保存HTML的目录
                        save_dir = "知乎回答HTML"
                        if not os.path.exists(save_dir):
                            os.makedirs(save_dir)
                            
                        # 如果有回答，依次获取每个回答的HTML
                        if answer_urls:
                            for i, answer_url in enumerate(answer_urls, 1):
                                print(f"\n处理第 {i} 个回答：{answer_url}")
                                
                                # 在访问回答链接前先进行一些随机操作
                                random_sleep(2, 4)
                                simulate_human_behavior(driver)
                                
                                # 打开回答页面
                                driver.get(answer_url)
                                print("已打开回答页面")
                                
                                # 等待页面加载
                                random_sleep(2, 3)
                                simulate_human_behavior(driver)
                                
                                # 对回答页面进行截图
                                screenshot_filename = take_screenshot(driver, f"answer_{i}")
                                if screenshot_filename:
                                    article["pic_answer"].append(screenshot_filename)
                                
                                # 获取页面源码
                                page_source = driver.page_source
                                
                                # 生成文件名（使用时间戳避免文件名冲突）
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                filename = os.path.join(save_dir, f"回答_{i}_{timestamp}.html")
                                
                                # 保存HTML文件
                                with open(filename, 'w', encoding='utf-8') as f:
                                    f.write(page_source)
                                print(f"已保存HTML到：{filename}")
                                
                                # 解析HTML文件获取作者和内容
                                author, texts = parse_answer(filename)
                                if author:
                                    article["author"].append(author)
                                    print(f"已添加作者：{author}")
                                else:
                                    article["author"].append("未知作者")
                                    print("未找到作者信息")
                                
                                if texts:
                                    article["content"].append(texts)
                                    print(f"已添加 {len(texts)} 段文本内容")
                                else:
                                    article["content"].append([])
                                    print("未找到文本内容")
                                
                            print(f"\n总共保存了 {len(answer_urls)} 个回答的HTML文件")
                            print(f"总共解析了 {len(article['author'])} 个作者")
                            print(f"总共解析了 {len(article['content'])} 个回答内容")
                            
                            # 保存article数据为JSON
                            saved_json = save_article_json(article)
                            print("任务完成！")
                            
                        else:
                            print("没有找到任何回答URL")
                        
                    except Exception as e:
                        print("获取问题标题失败：", e)
                    
                except json.JSONDecodeError as e:
                    print("解析AI返回的JSON失败:", e)
                except KeyError as e:
                    print("获取选中文章信息失败:", e)
            
        else:
            print("未获取到热榜内容")
        
    except Exception as e:
        print(f"发生错误: {e}")
    
    finally:
        print("正在关闭浏览器...")
        driver.quit()

if __name__ == "__main__":
    main() 