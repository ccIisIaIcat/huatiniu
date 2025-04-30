from moviepy.editor import VideoFileClip
import os

def process_video(input_path, output_path, speed_factor=2.0, remove_audio=True):
    """
    处理视频：加速和移除音频
    
    参数:
    input_path: 输入视频路径
    output_path: 输出视频路径
    speed_factor: 加速倍数，默认2倍速
    remove_audio: 是否移除音频，默认True
    """
    try:
        # 加载视频
        video = VideoFileClip(input_path)
        
        # 加速视频
        fast_video = video.speedx(speed_factor)
        
        # 如果需要移除音频
        if remove_audio:
            fast_video = fast_video.without_audio()
            
        # 保存处理后的视频
        fast_video.write_videofile(output_path, 
                                 codec='libx264', 
                                 audio_codec=None if remove_audio else 'aac')
        
        # 清理
        video.close()
        fast_video.close()
        
        print(f"视频处理完成: {output_path}")
        
    except Exception as e:
        print(f"处理视频时出错: {str(e)}")
        if 'video' in locals():
            video.close()
        if 'fast_video' in locals():
            fast_video.close()

def batch_process_videos(input_dir, output_dir, speed_factor=2.0, remove_audio=True):
    """
    批量处理目录下的所有视频
    
    参数:
    input_dir: 输入视频目录
    output_dir: 输出视频目录
    speed_factor: 加速倍数，默认2倍速
    remove_audio: 是否移除音频，默认True
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 支持的视频格式
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv')
    
    # 遍历输入目录中的所有视频文件
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(video_extensions):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"fast_{filename}")
            
            print(f"正在处理: {filename}")
            process_video(input_path, output_path, speed_factor, remove_audio)

if __name__ == "__main__":
    # 示例用法
    input_dir = "cutmovie/output"  # 输入视频目录
    output_dir = "cutmovie/speed_up"  # 输出视频目录
    
    # 批量处理视频，2倍速，移除音频
    batch_process_videos(input_dir, output_dir, speed_factor=2.0, remove_audio=True) 