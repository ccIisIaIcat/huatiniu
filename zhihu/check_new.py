from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle
import random

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
        print("未找到Cookie文件")
        return False

def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 30)
    
    try:
        # 先访问知乎首页
        print("正在访问知乎首页...")
        driver.get("https://www.zhihu.com")
        random_sleep(2, 4)

        # 加载Cookie
        if load_cookies(driver):
            # 刷新页面使Cookie生效
            driver.refresh()
            random_sleep(2, 4)
            
            # 模拟人类行为
            simulate_human_behavior(driver)
            
            # 访问目标问题页面
            target_url = "https://www.zhihu.com/question/12318197776"
            print(f"正在访问：{target_url}")
            driver.get(target_url)
            
            # 随机等待并模拟人类行为
            random_sleep(3, 5)
            simulate_human_behavior(driver)
            
            # 获取问题标题
            try:
                title_element = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "QuestionHeader-title"))
                )
                print("\n问题标题：", title_element.text)
            except Exception as e:
                print("获取标题失败：", e)
            
            # 检查页面状态
            print("\n当前页面URL：", driver.current_url)
            
            input("按回车键退出...")
            
        else:
            print("请先运行主程序登录并保存Cookie")
    
    except Exception as e:
        print(f"发生错误: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
