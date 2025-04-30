from pydub import AudioSegment
import os

def slow_down_audio(input_path, output_path, speed_factor=0.8):
    """
    放慢音频速度
    
    Args:
        input_path: 输入音频文件路径
        output_path: 输出音频文件路径
        speed_factor: 速度因子，小于1表示放慢，大于1表示加快
    """
    # 加载音频文件
    audio = AudioSegment.from_file(input_path)
    
    # 计算新的采样率
    new_sample_rate = int(audio.frame_rate * speed_factor)
    
    # 使用帧率调整来改变速度
    slowed_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": new_sample_rate
    })
    
    # 设置新的帧率
    slowed_audio = slowed_audio.set_frame_rate(audio.frame_rate)
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 保存处理后的音频
    slowed_audio.export(output_path, format="wav")
    print(f"处理后的音频已保存为: {output_path}")

def main():
    # 设置输入输出路径
    input_path = "G:/cc/demo/tts/voice/article_20250428_151419.wav"
    output_path = "G:/cc/demo/tts/voice/slow_voice.wav"
    
    # 放慢音频速度（0.8倍速）
    slow_down_audio(input_path, output_path, speed_factor=0.9)

if __name__ == "__main__":
    main() 