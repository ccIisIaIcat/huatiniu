from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json
from datetime import datetime
import sys

def load_cookies():
    """加载保存的cookies"""
    cookies_file = os.path.join("G:\\cc", "demo", "bilibili", "temp", "bilibili_cookies.json")
    if os.path.exists(cookies_file):
        with open(cookies_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_auth_info(driver):
    """保存认证信息（cookies和localStorage）"""
    save_dir = os.path.join("G:\\cc", "demo", "bilibili", "temp")
    os.makedirs(save_dir, exist_ok=True)
    
    # 保存cookies
    cookies = driver.get_cookies()
    cookies_file = os.path.join(save_dir, "bilibili_cookies.json")
    with open(cookies_file, 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    print(f"Cookies已保存到: {cookies_file}")
    
    # 获取localStorage
    local_storage = driver.execute_script("return window.localStorage;")
    local_storage_file = os.path.join(save_dir, "bilibili_localStorage.json")
    with open(local_storage_file, 'w', encoding='utf-8') as f:
        json.dump(local_storage, f, ensure_ascii=False, indent=2)
    print(f"localStorage已保存到: {local_storage_file}")

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

def handle_notification_dialog(driver):
    """处理通知权限提示框"""
    try:
        wait = WebDriverWait(driver, 5)
        # 查找并点击允许按钮
        allow_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='允许']")))
        allow_btn.click()
        print("已点击允许通知")
        return True
    except:
        try:
            # 如果找不到按钮，尝试使用class name
            allow_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "allow-btn")))
            allow_btn.click()
            print("已点击允许通知")
            return True
        except Exception as e:
            print(f"处理通知权限提示框失败: {str(e)}")
            return False

def select_video_category(driver):
    """选择视频分区为知识分区"""
    try:
        wait = WebDriverWait(driver, 10)
        
        # 首先定位到分区选择器的容器并点击
        category_container = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 
            "div.video-human-type div.select-controller"
        )))
        driver.execute_script("arguments[0].click();", category_container)
        print("已点击分区选择框")
        
        time.sleep(2)  # 等待下拉菜单完全展开
        
        try:
            # 等待下拉菜单容器出现
            dropdown_container = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "div.drop-list-v2-container.human-type-list"
            )))
            
            # 直接查找知识分区选项
            knowledge_option = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "div.drop-list-v2-item[title='知识']"
            )))
            
            # 确保选项在视图中
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", knowledge_option)
            time.sleep(0.5)  # 等待滚动完成
            
            # 点击选项
            driver.execute_script("arguments[0].click();", knowledge_option)
            print("已选择知识分区")
            return True
                
        except Exception as inner_e:
            print(f"选择知识分区选项失败: {str(inner_e)}")
            return False
            
    except Exception as e:
        print(f"选择分区失败: {str(e)}")
        return False

def fill_video_info(driver, title="这是一个测试"):
    """填写视频信息"""
    try:
        wait = WebDriverWait(driver, 10)
        # 等待标题输入框出现并填写
        title_input = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 
            "input.input-val[placeholder='请输入稿件标题']"
        )))
        # 清除默认内容
        title_input.clear()
        # 输入新标题
        title_input.send_keys(title)
        print(f"已设置视频标题: {title}")
        
        # 等待一下确保输入完成
        time.sleep(1)
        
        # 选择知识分区
        if not select_video_category(driver):
            print("警告：分区选择失败")
        
        # 验证标题是否设置成功
        actual_title = title_input.get_attribute('value')
        if actual_title == title:
            print("标题设置成功，已验证")
        else:
            print(f"警告：标题可能未正确设置，当前值为: {actual_title}")
            
        return True
    except Exception as e:
        print(f"设置视频标题失败: {str(e)}")
        return False

def upload_video(driver, video_path):
    """上传视频文件"""
    try:
        # 等待上传按钮出现
        wait = WebDriverWait(driver, 10)
        
        # 首先等待上传区域可见
        upload_area = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
        
        # 直接发送文件路径到文件输入框
        upload_area.send_keys(video_path)
        print(f"已选择视频文件: {video_path}")
        
        # 等待一段时间让上传开始
        time.sleep(5)
        
        # 等待上传完成后填写视频信息
        fill_video_info(driver)
        
        return True
        
    except Exception as e:
        print(f"上传视频失败: {str(e)}")
        return False

def click_upload_button(driver):
    """点击投稿按钮并等待页面加载"""
    try:
        # 等待投稿按钮出现并点击
        wait = WebDriverWait(driver, 10)
        upload_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "header-upload-entry")))
        upload_btn.click()
        print("已点击投稿按钮")
        
        # 等待新页面加载（等待URL变化）
        time.sleep(3)  # 给页面跳转一些时间
        
        # 切换到新打开的标签页
        windows = driver.window_handles
        if len(windows) > 1:
            driver.switch_to.window(windows[-1])
            
        # 等待投稿页面加载完成
        wait.until(lambda d: "member.bilibili.com" in d.current_url)
        print("已进入投稿页面")
        return True
        
    except Exception as e:
        print(f"处理投稿页面失败: {str(e)}")
        return False

def open_bilibili():
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    # 自动允许通知权限
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1  # 1允许，2阻止
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
                save_auth_info(driver)  # 保存认证信息
                # 尝试点击投稿按钮
                if click_upload_button(driver):
                    return driver
            else:
                print("cookies已失效，需要重新登录...")
                driver.delete_all_cookies()
                driver.refresh()
                time.sleep(2)
        
        # 如果没有cookies或cookies失效，进行手动登录
        print("请完成手动登录...")
        
        # 等待登录完成
        while not check_login_status(driver):
            time.sleep(2)  # 每2秒检查一次登录状态
            
        print("登录成功！")
        # 保存新的认证信息
        save_auth_info(driver)
        # 尝试点击投稿按钮
        if click_upload_button(driver):
            return driver
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        driver.quit()
        return None

def check_already_uploaded(json_name):
    """检查是否已经上传过"""
    already_path = os.path.join("G:\\cc", "demo", "bilibili", "already", f"{json_name}")
    return os.path.exists(already_path)

def get_video_info(json_name):
    """从JSON文件获取视频信息"""
    try:
        json_path = os.path.join("G:\\cc", "demo", "zhihu", "article", json_name)
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('title')
    except Exception as e:
        print(f"读取JSON文件失败: {str(e)}")
        return None

def mark_as_uploaded(json_name):
    """标记为已上传"""
    try:
        already_dir = os.path.join("G:\\cc", "demo", "bilibili", "already")
        os.makedirs(already_dir, exist_ok=True)
        already_path = os.path.join(already_dir, json_name)
        # 创建一个空文件作为标记
        with open(already_path, 'w') as f:
            pass
        print(f"已标记为已上传: {json_name}")
    except Exception as e:
        print(f"标记上传状态失败: {str(e)}")

def process_video(json_name):
    """处理视频上传任务"""
    # 检查是否已上传
    if check_already_uploaded(json_name):
        print(f"视频已经上传过: {json_name}")
        return False
        
    # 获取视频标题
    title = get_video_info(json_name)
    if not title:
        print("获取视频信息失败")
        return False
        
    # 构建视频文件路径
    video_name = json_name.replace('.json', '.mp4')
    video_path = os.path.join("G:\\cc", "demo", "cutmovie", "add_music", video_name)
    
    if not os.path.exists(video_path):
        print(f"视频文件不存在: {video_path}")
        return False
        
    # 初始化浏览器并打开上传页面
    driver = open_bilibili()
    if not driver:
        return False
        
    try:
        # 等待上传区域出现
        wait = WebDriverWait(driver, 10)
        upload_area = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
        
        # 上传视频文件
        print(f"开始上传视频: {video_path}")
        upload_area.send_keys(video_path)
        print("已选择视频文件")
        
        # 等待上传开始
        time.sleep(5)
        
        # 设置视频标题和分区
        print(f"正在设置视频标题: {title}")
        if not fill_video_info(driver, title):
            print("设置视频信息失败")
            return False
            
        print("视频信息设置成功")
        
        # 等待上传完成
        print("等待视频上传完成...")
        wait = WebDriverWait(driver, 600)  # 最多等待10分钟
        upload_success = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//span[contains(@class, 'success') and contains(text(), '上传完成')]"
        )))
        print("视频上传完成")
        
        # 点击立即投稿按钮
        submit_button = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//span[contains(@class, 'submit-add')]"
        )))
        submit_button.click()
        print("已点击投稿按钮")
        
        # 等待10秒
        time.sleep(15)
        
        # 标记为已上传
        mark_as_uploaded(json_name)
        print("已标记为已上传")
        return True

    except Exception as e:
        print(f"上传过程中出错: {str(e)}")
        return False
    finally:
        driver.quit()
        print("浏览器已关闭")

if __name__ == "__main__":        
    json_name = "article_20250428_212036.json"
    if not json_name.endswith('.json'):
        json_name += '.json'
        
    if process_video(json_name):
        print("视频上传任务完成")
    else:
        print("视频上传任务失败")
