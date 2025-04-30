import os
import time
from upload import process_video

def get_all_json_files():
    """获取所有待上传的JSON文件"""
    article_dir = os.path.join("G:\\cc", "demo", "zhihu", "article")
    json_files = []
    
    # 获取目录下所有JSON文件
    for file in os.listdir(article_dir):
        if file.endswith('.json'):
            json_files.append(file)
            
    return sorted(json_files)  # 按文件名排序

def batch_upload():
    """批量上传视频"""
    json_files = get_all_json_files()
    
    if not json_files:
        print("没有找到需要上传的JSON文件")
        return
        
    print(f"找到 {len(json_files)} 个待上传文件")
    
    for i, json_file in enumerate(json_files, 1):
        print(f"\n开始处理第 {i}/{len(json_files)} 个文件: {json_file}")
        
        try:
            if process_video(json_file):
                print(f"文件 {json_file} 上传成功")
            else:
                print(f"文件 {json_file} 上传失败")
        except Exception as e:
            print(f"处理文件 {json_file} 时发生错误: {str(e)}")
        
        # 每个文件之间暂停30秒
        if i < len(json_files):
            print("等待5秒后继续下一个文件...")
            time.sleep(5)

if __name__ == "__main__":
    print("开始批量上传视频...")
    batch_upload()
    print("\n批量上传任务完成") 