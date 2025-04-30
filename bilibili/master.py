from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import json

def load_cookies():
    """加载保存的cookies"""
    cookies_file = os.path.join("G:\\cc", "demo", "bilibili", "temp", "bilibili_cookies.json")
    if os.path.exists(cookies_file):
        with open(cookies_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def check_login_status(driver):
    """检查是否已登录"""
    try:
        # 检查登录按钮是否存在
        login_buttons = driver.find_elements(By.CLASS_NAME, "header-login-entry")
        if not login_buttons:  # 如果找不到登录按钮，说明已经登录
            return True
        return False
    except:
        return False

def save_cookies(driver):
    """保存cookies"""
    cookies_dir = os.path.join("G:\\cc", "demo", "bilibili", "temp")
    os.makedirs(cookies_dir, exist_ok=True)
    cookies_file = os.path.join(cookies_dir, "bilibili_cookies.json")
    
    cookies = driver.get_cookies()
    with open(cookies_file, 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    print(f"Cookies已保存到: {cookies_file}")

def login_bilibili():
    """使用cookies登录B站"""
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
    })
    
    # 创建Chrome WebDriver实例
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # 打开B站
        driver.get('https://www.bilibili.com/')
        time.sleep(2)
        
        # 检查是否存在cookies文件
        cookies = load_cookies()
        if cookies:
            print("发现已保存的cookies，尝试使用...")
            # 添加cookies
            for cookie in cookies:
                try:
                    driver.add_cookie(cookie)
                except:
                    continue
            
            # 刷新页面以应用cookies
            driver.refresh()
            time.sleep(3)
            
            # 检查登录状态
            if check_login_status(driver):
                print("自动登录成功！")
                return driver
            else:
                print("cookies已失效，需要重新登录...")
                driver.delete_all_cookies()
                driver.refresh()
        else:
            print("未找到cookies文件")
            
        print("请手动完成登录...")
        # 等待手动登录完成
        while not check_login_status(driver):
            time.sleep(2)
            
        print("登录成功！")
        # 保存新的cookies
        save_cookies(driver)
        return driver
        
    except Exception as e:
        print(f"登录过程中出错: {str(e)}")
        driver.quit()
        return None

if __name__ == "__main__":
    print("开始登录B站...")
    driver = login_bilibili()
    if driver:
        print("登录成功，请保持窗口打开")
        # 保持窗口打开，等待用户手动关闭
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n正在关闭浏览器...")
            driver.quit()
    else:
        print("登录失败")
