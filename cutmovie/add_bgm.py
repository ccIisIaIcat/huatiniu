import os
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from pathlib import Path
import random
import os
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_audioclips
from pathlib import Path
import random

def loop_audio_to_length(audio_clip, target_duration):
    """循环补足音频到目标时长"""
    clips = []
    total = 0
    while total < target_duration:
        remain = target_duration - total
        seg = audio_clip.subclip(0, min(remain, audio_clip.duration))
        clips.append(seg)
        total += seg.duration
    return concatenate_audioclips(clips)

def main():
    output_dir = Path("G:/cc/demo/cutmovie/output")
    music_dir = Path("G:/cc/demo/cutmovie/music")
    add_music_dir = Path("G:/cc/demo/cutmovie/add_music")
    add_music_dir.mkdir(exist_ok=True)

    # 获取所有视频和音乐文件
    video_files = list(output_dir.glob("*.mp4"))
    music_files = list(music_dir.glob("*.mp3")) + list(music_dir.glob("*.wav"))
    if not music_files:
        print("未找到背景音乐文件！")
        return

    # 获取已处理过的视频文件名
    done_files = set([f.name for f in add_music_dir.glob("*.mp4")])

    for video_file in video_files:
        if video_file.name in done_files:
            print(f"已存在: {video_file.name}，跳过")
            continue
        print(f"处理: {video_file.name}")
        video = VideoFileClip(str(video_file))
        # 随机选一首背景音乐
        music_file = random.choice(music_files)
        bgm = AudioFileClip(str(music_file))
        # 循环补足音乐长度
        if bgm.duration < video.duration:
            n = int(video.duration // bgm.duration) + 1
            bgm = concatenate_audioclips([bgm] * n).subclip(0, video.duration)
        else:
            bgm = bgm.subclip(0, video.duration)
        # 降低背景音乐音量
        bgm = bgm.volumex(0.05)
        # 合成音频
        if video.audio is not None:
            new_audio = CompositeAudioClip([video.audio, bgm])
        else:
            new_audio = bgm
        # 设置新音频
        video_with_bgm = video.set_audio(new_audio)
        # 输出
        out_path = add_music_dir / video_file.name
        video_with_bgm.write_videofile(str(out_path), codec="libx264", audio_codec="aac")
        print(f"已输出: {out_path}")

if __name__ == "__main__":
    main() 