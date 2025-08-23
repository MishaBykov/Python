import argparse
import os
import subprocess
import concurrent.futures
from typing import List, Tuple, Optional


def parse_args():
    parser = argparse.ArgumentParser(
        description='Merge mkv video and audio, and subs. Audio and subs Contain the prefix name of the video file')
    parser.add_argument("--dir_mkvmerge", type=str, help="directory mkvmerge", default="", required=False)
    parser.add_argument("--video_input", type=str, help="directory video")
    parser.add_argument("--audio_input", type=str, help="directory audio")
    parser.add_argument("--subs_input", type=str, help="directory subs", required=False)
    parser.add_argument("--dir_output", type=str, help="directory output")
    parser.add_argument("--mkvmerge_prefix", type=str, help="prefix mkvmerge executable file", default="mkvmerge",
                        required=False)
    parser.add_argument("--max_workers", type=int, help="maximum number of parallel processes", default=4,
                        required=False)
    return parser.parse_args()


def find_tool_name(dir_tool: str, tool_prefix: str, tool_name: str) -> str:
    if not dir_tool:
        return tool_name  # Используем системный путь

    files = os.listdir(dir_tool)
    tool_list = list(filter(lambda s: s.startswith(tool_prefix), files))

    if len(tool_list) == 0:
        print(f"not found {tool_prefix} in {dir_tool}")
        return tool_name
    if len(tool_list) != 1:
        print(f"many found {tool_prefix} in {dir_tool}, using first")

    return tool_list[0]


def collect_video_audio_files_by_name(dir_video: str, dir_audio: str, dir_subs: Optional[str]) \
        -> List[Tuple[str, Optional[str], Optional[str]]]:
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


def process_file_wrapper(params):
    """Обертка для вызова process_file с распаковкой параметров"""
    return process_file(*params)


def run_command(cmd, description=""):
    """Запускает команду с правильной кодировкой"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', check=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error {description}: {e.stderr}")
        raise
    except Exception as e:
        print(f"Unexpected error {description}: {e}")
        raise


def process_file(args_tuple: Tuple[str, Optional[str], Optional[str]],
                 mkvmerge_path: str,
                 video_input: str,
                 audio_input: str,
                 subs_input: Optional[str],
                 dir_output: str) -> bool:
    """Обрабатывает один файл с помощью mkvmerge и возвращает успешность выполнения"""
    video_name, audio_name, sub_name = args_tuple

    path_video = os.path.join(video_input, video_name)
    if not os.path.exists(path_video):
        print(f"video not found: {path_video}")
        return False

    if audio_name is None:
        print(f"audio not found for video: {video_name}")
        return False

    path_audio = os.path.join(audio_input, audio_name)
    if not os.path.exists(path_audio):
        print(f"audio not found: {path_audio}")
        return False

    # Строим команду mkvmerge
    args_for_process = [
        mkvmerge_path,
        '-o', os.path.join(dir_output, video_name),
        '--no-audio',  # игнорируем аудио из видео файла
        path_video,
        '--language', '0:rus',  # устанавливаем язык для аудио
        '--default-track', '0:yes',  # устанавливаем как default
        path_audio
    ]

    if sub_name is not None and subs_input is not None:
        path_sub = os.path.join(subs_input, sub_name)
        if os.path.exists(path_sub):
            args_for_process.extend([
                '--language', '0:rus',  # язык для субтитров
                path_sub
            ])
        else:
            print(f"sub({path_sub}) not found")

    try:
        print(f"Processing with mkvmerge: {video_name}")
        print(f"Command: {' '.join(args_for_process)}")

        result = run_command(args_for_process, f"processing {video_name}")

        if result.returncode == 0:
            print(f"Completed: {video_name}")

            # Проверяем результат с помощью mkvmerge
            check_cmd = [mkvmerge_path, '-i', os.path.join(dir_output, video_name)]
            check_result = run_command(check_cmd, f"checking {video_name}")

            print(f"Output file info for {video_name}:")
            print(check_result.stdout)
            if check_result.stderr:
                print(check_result.stderr)

            return True
        else:
            print(f"mkvmerge error for {video_name}: {result.stderr}")
            return False

    except subprocess.CalledProcessError as e:
        print(f"Error processing {video_name}: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error processing {video_name}: {e}")
        return False


if __name__ == '__main__':
    args = parse_args()

    # Ищем mkvmerge
    mkvmerge_name = find_tool_name(args.dir_mkvmerge, args.mkvmerge_prefix, 'mkvmerge')
    if args.dir_mkvmerge:
        mkvmerge_path = os.path.join(args.dir_mkvmerge, mkvmerge_name)
    else:
        mkvmerge_path = mkvmerge_name  # Используем из системного PATH

    # Проверяем доступность mkvmerge
    try:
        version_check = run_command([mkvmerge_path, '--version'], "checking mkvmerge version")
        if version_check.returncode != 0:
            print(f"mkvmerge not found or not working: {mkvmerge_path}")
            print("Please install mkvtoolnix or specify --dir_mkvmerge")
            exit(1)
        print(f"Using mkvmerge: {version_check.stdout.splitlines()[0]}")
    except:
        print(f"mkvmerge not found or not working: {mkvmerge_path}")
        print("Please install mkvtoolnix or specify --dir_mkvmerge")
        exit(1)

    # Создаем выходную директорию если не существует
    os.makedirs(args.dir_output, exist_ok=True)

    video_audio_sub_name = collect_video_audio_files_by_name(
        args.video_input, args.audio_input, args.subs_input
    )

    # Запускаем обработку файлов параллельно с использованием ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        # Подготавливаем аргументы для каждой задачи
        tasks = [
            (file_tuple, mkvmerge_path, args.video_input, args.audio_input, args.subs_input, args.dir_output)
            for file_tuple in video_audio_sub_name
        ]

        # Запускаем все задачи
        results = list(executor.map(process_file_wrapper, tasks))

    # Выводим статистику
    successful = sum(results)
    total = len(results)
    print(f"\nProcessing completed: {successful}/{total} files processed successfully with mkvmerge")