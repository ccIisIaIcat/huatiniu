from moviepy.editor import *
import os
from pathlib import Path
import sys

def create_video(audio_dir, pic_dir, output_dir):
    try:
        # 设置路径
        audio_dir = Path(audio_dir)
        pic_dir = Path(pic_dir)
        output_dir = Path(output_dir)
        
        # 获取所有音频文件
        audio_files = sorted(list(audio_dir.glob("*.wav")))
        if not audio_files:
            print("错误：未找到音频文件")
            return
        
        # 获取所有图片文件
        pic_files = sorted(list(pic_dir.glob("*.png")))
        if not pic_files:
            print("错误：未找到图片文件")
            return
        
        print(f"找到 {len(audio_files)} 个音频文件和 {len(pic_files)} 个图片文件")
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 处理每个音频文件
        for i, audio_file in enumerate(audio_files):
            try:
                print(f"\n处理第 {i+1}/{len(audio_files)} 个文件: {audio_file.name}")
                
                # 加载音频
                audio = AudioFileClip(str(audio_file))
                
                # 选择对应的图片（循环使用）
                pic_file = pic_files[i % len(pic_files)]
                print(f"使用图片: {pic_file.name}")
                
                # 创建图片剪辑
                image = ImageClip(str(pic_file))
                
                # 设置图片持续时间与音频相同
                image = image.set_duration(audio.duration)
                
                # 将音频添加到图片
                video = image.set_audio(audio)
                
                # 生成输出文件名
                output_file = output_dir / f"video_{i+1}.mp4"
                
                # 导出视频
                print("正在生成视频...")
                video.write_videofile(
                    str(output_file),
                    fps=24,
                    codec='libx264',
                    audio_codec='aac',
                    temp_audiofile='temp-audio.m4a',
                    remove_temp=True,
                    verbose=False,
                    logger=None
                )
                
                print(f"✓ 已生成视频: {output_file}")
                
            except Exception as e:
                print(f"处理文件 {audio_file.name} 时出错: {str(e)}")
                continue
            
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return

def main():
    # 设置路径
    audio_dir = "G:/cc/demo/tts/voice"
    pic_dir = "G:/cc/demo/zhihu/pic"
    output_dir = "G:/cc/demo/cutmovie/output"
    
    print("开始处理视频...")
    create_video(audio_dir, pic_dir, output_dir)
    print("\n处理完成！")

if __name__ == "__main__":
    main()
