import argparse
import os
import subprocess


def parse_args():
    parser = argparse.ArgumentParser(
        description='Merge mkv video and audio, and subs. Audio and subs Contain the prefix name of the video file')
    parser.add_argument("--dir_ffmpeg", type=str, help="directory ffmpeg")
    parser.add_argument("--video_input", type=str, help="directory video")
    parser.add_argument("--audio_input", type=str, help="directory audio")
    parser.add_argument("--subs_input", type=str, help="directory subs", required=False)
    parser.add_argument("--dir_output", type=str, help="directory output")
    parser.add_argument("--ffmpeg_prefix", type=str, help="prefix ffmpeg executable file", default="ffmpeg",
                        required=False)
    return parser.parse_args()


def find_ffmpeg_name(dir_ffmpeg: str):
    os.listdir(dir_ffmpeg)
    ffmpeg_list = list(filter(lambda s: s.startswith('ffmpeg'), os.listdir(dir_ffmpeg)))

    if len(ffmpeg_list) == 0:
        print("not fount " + ffmpeg_prefix)
        exit(1)
    if len(ffmpeg_list) != 1:
        print("many fount " + ffmpeg_prefix)
        exit(1)

    return ffmpeg_list[0]


def collect_video_audio_files_by_name(dir_video: str, dir_audio: str, dir_subs: str | None) \
        -> list[tuple[str, str | None, str | None]]:
    result = []
    for video_name_file in os.listdir(dir_video):
        if os.path.splitext(video_name_file)[1] != '.mkv':
            continue
        video_name = os.path.splitext(video_name_file)[0]
        fined_audio_file = None
        fined_sub_file = None
        for audio_name_file in os.listdir(dir_audio):
            if audio_name_file.startswith(video_name):
                fined_audio_file = audio_name_file
                break
        if dir_subs is not None:
            for sub_name_file in os.listdir(dir_subs):
                if sub_name_file.startswith(video_name):
                    fined_sub_file = sub_name_file
                    break
        result.append((video_name_file, fined_audio_file, fined_sub_file))
    return result


if __name__ == '__main__':
    args = parse_args()

    ffmpeg_prefix = args.ffmpeg_prefix
    ffmpeg_path = os.path.join(args.dir_ffmpeg, find_ffmpeg_name(args.dir_ffmpeg))

    if not os.path.exists(ffmpeg_path):
        print("ffmpeg not found")
        exit()

    video_audio_sub_name = collect_video_audio_files_by_name(args.video_input, args.audio_input, args.subs_input)

    for video_name, audio_name, sub_name in video_audio_sub_name:

        path_video = os.path.join(args.video_input, video_name)
        if not os.path.exists(path_video):
            print("video not found")
            continue

        path_audio = os.path.join(args.audio_input, audio_name)
        if not os.path.exists(path_audio):
            print("audio not found")
            continue

        args_for_process = [ffmpeg_path,
                            '-i', path_video,
                            '-i', path_audio,
                            '-map', '0',
                            '-map', '1',
                            '-c', 'copy', os.path.join(args.dir_output, video_name)]

        if sub_name is not None:
            path_sub = os.path.join(args.subs_input, sub_name)
            if not os.path.exists(path_sub):
                print(f"sub({path_sub}) not found")
            else:
                args_for_process = args_for_process[:9] + ['-map', '2'] + args_for_process[9:]
                args_for_process = args_for_process[:5] + ['-i', path_sub] + args_for_process[5:]

        subprocess.run(args_for_process)
