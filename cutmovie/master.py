import sys
import json
from pathlib import Path
import pandas as pd
import numpy as np
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips
import os

def main(json_filename):
    article_path = Path("G:/cc/demo/zhihu/article") / json_filename
    check_path = Path("G:/cc/demo/check/check") / json_filename
    voice_dir = Path("G:/cc/demo/tts/voice")
    base_name = Path(json_filename).stem

    # 读取article json
    if not article_path.exists():
        print(f"未找到文件: {article_path}")
        return
    with open(article_path, 'r', encoding='utf-8') as f:
        article_data = json.load(f)
    if not check_path.exists():
        print(f"未找到文件: {check_path}")
        return
    with open(check_path, 'r', encoding='utf-8') as f:
        check_list = json.load(f)

    content_list = article_data.get('content', [])
    intro_pic_list = article_data.get('pic_tittle', [])
    ans_pic_list = article_data.get('pic_answer', [])
    outro_pic_list = article_data.get('pic_tittle', [])
    part_count = len(content_list)

    # 生成应有的音频文件名
    filenames = []
    intro_name = f"{base_name}_intro.wav"
    filenames.append(intro_name)
    for i in range(1, part_count+1):
        filenames.append(f"{base_name}_part{i}.wav")
    outtro_name = f"{base_name}_outro.wav"
    filenames.append(outtro_name)
    temp_df = pd.DataFrame(np.array([filenames,intro_pic_list+ans_pic_list+outro_pic_list,[True]+check_list+[True]]).T)
    temp_df.columns = ["音频文件名","图片文件名","是否需要生成"]
    temp_df = temp_df[temp_df["是否需要生成"]=="True"]
    
    print(len(filenames))
    print(len(intro_pic_list+ans_pic_list))

    # 合成视频片段并拼接
    output_dir = Path("G:/cc/demo/cutmovie/output")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{base_name}.mp4"
    clips = []
    for idx, row in temp_df.iterrows():
        audio_path = voice_dir / row["音频文件名"]
        img_path = Path("G:/cc/demo/zhihu/pic") / row["图片文件名"]
        if not audio_path.exists() or not img_path.exists():
            print(f"缺失文件: {audio_path} 或 {img_path}")
            continue
        audio = AudioFileClip(str(audio_path))
        image = ImageClip(str(img_path)).set_duration(audio.duration)
        video = image.set_audio(audio)
        clips.append(video)
    if clips:
        final_clip = concatenate_videoclips(clips)
        print(f"正在导出: {output_path}")
        final_clip.write_videofile(str(output_path), fps=24, codec='libx264', audio_codec='aac')
        print("导出完成！")
    else:
        print("没有可合成的视频片段。")

if __name__ == "__main__":
    article_dir = "G:/cc/demo/zhihu/article"
    json_files = [f for f in os.listdir(article_dir) if f.endswith('.json')]
    if not json_files:
        raise FileNotFoundError("未找到任何json文件")
    json_files.sort()
    json_name = json_files[-1]
    main(json_name)
