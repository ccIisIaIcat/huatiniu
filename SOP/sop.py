import shutil
from pathlib import Path
import os

def step0():
    folders = [
        r'G:/cc/demo/check/check',
        r'G:/cc/demo/cutmovie/output',
        r'G:/cc/demo/cutmovie/add_music',
        r'G:/cc/demo/tts/voice',
        r'G:/cc/demo/zhihu/article',
        r'G:/cc/demo/zhihu/pic',
        r'G:/cc/demo/zhihu/知乎回答HTML',
        r'G:/cc/demo/zhihu/知乎热榜数据',
        r'G:/cc/demo/zhihu/知乎页面分析',
    ]
    for folder in folders:
        p = Path(folder)
        if p.exists() and p.is_dir():
            for item in p.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
    print('已清空所有指定文件夹内容')
    


def step1():
    # 切换到zhihu目录，运行zhihu_selenium.py，运行完再切回SOP目录
    origin = os.getcwd()
    zhihu_dir = r'G:/cc/demo/zhihu'
    sop_dir = r'G:/cc/demo/SOP'
    os.chdir(zhihu_dir)
    print(f"切换到目录: {zhihu_dir}")
    os.system('python zhihu_selenium.py')
    os.chdir(sop_dir)
    print(f"已切回目录: {sop_dir}")
    
def step2():
    # 切换到check目录，运行check.py，运行完再切回SOP目录
    origin = os.getcwd()
    check_dir = r'G:/cc/demo/check'
    sop_dir = r'G:/cc/demo/SOP'
    os.chdir(check_dir)
    print(f"切换到目录: {check_dir}")
    os.system('python check.py')
    os.chdir(sop_dir)
    print(f"已切回目录: {sop_dir}")

def step3():
    # 切换到tts目录，运行master.py，运行完再切回SOP目录
    origin = os.getcwd()
    tts_dir = r'G:/cc/demo/tts'
    sop_dir = r'G:/cc/demo/SOP'
    os.chdir(tts_dir)
    print(f"切换到目录: {tts_dir}")
    os.system('python master.py')
    os.chdir(sop_dir)
    print(f"已切回目录: {sop_dir}")

def step4():
    # 切换到cutmovie目录，运行master.py，运行完再切回SOP目录
    origin = os.getcwd()
    cutmovie_dir = r'G:/cc/demo/cutmovie'
    sop_dir = r'G:/cc/demo/SOP'
    os.chdir(cutmovie_dir)
    print(f"切换到目录: {cutmovie_dir}")
    os.system('python master.py')
    os.chdir(sop_dir)
    print(f"已切回目录: {sop_dir}")
    
def step5():
    # 切换到cutmovie目录，运行add_bgm.py，运行完再切回SOP目录
    origin = os.getcwd()
    cutmovie_dir = r'G:/cc/demo/cutmovie'
    sop_dir = r'G:/cc/demo/SOP'
    os.chdir(cutmovie_dir)
    print(f"切换到目录: {cutmovie_dir}")
    os.system('python add_bgm.py')
    os.chdir(sop_dir)
    print(f"已切回目录: {sop_dir}")

def step6():
    # 切换到bilibili目录，运行batch_upload.py，运行完再切回SOP目录
    origin = os.getcwd()
    bilibili_dir = r'G:/cc/demo/bilibili'
    sop_dir = r'G:/cc/demo/SOP'
    os.chdir(bilibili_dir)
    print(f"切换到目录: {bilibili_dir}")
    os.system('python batch_upload.py')
    os.chdir(sop_dir)
    print(f"已切回目录: {sop_dir}")

step0()
# for i in range(15):
#     step1()
#     step2()
#     step3()
#     step4()
#     step5()
    
# step1()
# step2()
# step3()
# step4()
# step5()
# step6()

