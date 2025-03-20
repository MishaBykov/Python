import argparse
import os
import subprocess


def parse_args():
    parser = argparse.ArgumentParser(description='Merge mkv video and audio. Names must match')
    parser.add_argument("dir_ffmpeg", type=str, help="directory ffmpeg")
    parser.add_argument("video_input", type=str, help="directory video")
    parser.add_argument("audio_input", type=str, help="directory audio")
    parser.add_argument("dir_output", type=str, help="directory output")
    parser.add_argument("ffmpeg_prefix", type=str, help="prefix ffmpeg executable file", default="ffmpeg",
                        required=False)
    return parser.parse_args()


def find_ffmpeg_name(dir_ffmpeg):
    os.listdir(dir_ffmpeg)
    ffmpeg_list = list(filter(lambda s: s.startswith('ffmpeg'), os.listdir(dir_ffmpeg)))

    if len(ffmpeg_list) == 0:
        print("not fount " + ffmpeg_prefix)
        exit(1)
    if len(ffmpeg_list) != 1:
        print("many fount " + ffmpeg_prefix)
        exit(1)

    return ffmpeg_list[0]


def collect_video_and_audio_files(dir_video, dir_audio) -> dict:
    result = {}
    for video_name_file in os.listdir(dir_video):
        key = os.path.splitext(video_name_file)[0]
        result[key] = video_name
    for audio_name_file in os.listdir(dir_audio):
        key = os.path.splitext(audio_name_file)[0]
        video_name_file = result[key]
        result[key] = (video_name_file, audio_name_file)
    return result


if __name__ == '__main__':
    args = parse_args()

    ffmpeg_prefix = args.ffmpeg_prefix
    ffmpeg_path = os.path.join(args.dir_ffmpeg, find_ffmpeg_name(args.dir_ffmpeg))

    if not os.path.exists(ffmpeg_path):
        print("ffmpeg not found")
        exit()

    name_video_audio_dict = collect_video_and_audio_files(args.dir_video, args.dir_audio)

    for video_name, audio_name in name_video_audio_dict.values():
        path_video = os.path.join(args.dir_video, video_name)
        if not os.path.exists(path_video):
            print("video not found")
            continue

        path_audio = os.path.join(args.dir_audio, audio_name)
        if not os.path.exists(path_audio):
            print("audio not found")
            continue

        subprocess.run([ffmpeg_path,
                        '-i', path_video,
                        '-i', path_audio,
                        '-map', '0',
                        '-map', '1',
                        '-c', 'copy', os.path.join(args.dir_output, video_name)])
