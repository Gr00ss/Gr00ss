from datetime import datetime
import os
import shutil
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

load_dotenv()
if os.getenv('GITHUB_TOKEN'):
    os.environ['GITHUB_TOKEN'] = os.getenv('GITHUB_TOKEN')

import gifos

FONT_FILE_LOGO = "./fonts/vtks-blocketo.regular.ttf"
# FONT_FILE_BITMAP = "./fonts/ter-u14n.pil"
FONT_FILE_BITMAP = "./fonts/UnifontExMono.ttf"
FONT_FILE_TRUETYPE = "./fonts/IosevkaTermNerdFont-Bold.ttf"
FONT_FILE_MONA = "./fonts/Inversionz.otf"


def main():
    # Очищаем папку frames перед началом работы
    if os.path.exists("frames"):
        shutil.rmtree("frames")
    os.makedirs("frames", exist_ok=True)
    
    t = gifos.Terminal(750, 500, 15, 15, FONT_FILE_BITMAP, 15)

    t.gen_text("", 1, count=20)
    t.toggle_show_cursor(False)
    year_now = datetime.now(ZoneInfo("UTC")).strftime("%Y")
    t.gen_text("ZOV_OS Modular BIOS v1.4.8.8", 1)
    t.gen_text(f"Copyright (C) {year_now}, \x1b[31mGr00ss Softwares Inc.\x1b[0m", 2)
    t.gen_text("\x1b[30;101mCARDIOSTIMULATOR TERMINAL OF WAGNER ENJOYER, REV 7.1.5\x1b[0m", 4)
    t.gen_text("Peremoga(tm) GIFCPU - 4308Hz", 6)
    t.gen_text(
        "Press \x1b[91mDEL\x1b[0m to enter SETUP, \x1b[91mESC\x1b[0m to cancel Memory Test",
        t.num_rows,
    )
    for i in range(0, 32768, 3276):  # 32GB Memory
        t.delete_row(7)
        if i < 16384:
            t.gen_text(
                f"Memory Test: {i}MB", 7, count=2, contin=True
            )  # slow down upto a point
        else:
            t.gen_text(f"Memory Test: {i}MB", 7, contin=True)
    t.delete_row(7)
    t.gen_text("Memory Test: 32GB OK", 7, count=10, contin=True)
    t.gen_text("", 11, count=10, contin=True)

    t.clear_frame()
    t.gen_text("Initiating Boot Sequence ", 1, contin=True)
    t.gen_typing_text(".....", 1, contin=True)
    t.gen_text("\x1b[96m", 1, count=0, contin=True)
    
    os_logo_lines = [
        "//////////////////////////////////////////////////////////",
        "//                                                      //",
        "//   ███████╗ ██████╗ ██╗   ██╗     ██████╗ ███████╗    //",
        "//   ╚══███╔╝██╔═══██╗██║   ██║    ██╔═══██╗██╔════╝    //",
        "//     ███╔╝ ██║   ██║██║   ██║    ██║   ██║███████╗    //",
        "//    ███╔╝  ██║   ██║╚██╗ ██╔╝    ██║   ██║╚════██║    //",
        "//   ███████╗╚██████╔╝ ╚████╔╝     ╚██████╔╝███████║    //",
        "//   ╚══════╝ ╚═════╝   ╚═══╝       ╚═════╝ ╚══════╝    //",
        "//                                                      //",
        "//////////////////////////////////////////////////////////"
    ]
    
    # Вычисляем позицию для центрирования
    start_row = (t.num_rows - len(os_logo_lines)) // 2
    
    # Простое появление логотипа с красным цветом (в 5 раз быстрее)
    for line_idx, line in enumerate(os_logo_lines):
        t.gen_text(f"\x1b[91m{line}\x1b[0m", start_row + line_idx + 1, 1)

    t.clear_frame()
    t.clone_frame(5)
    t.toggle_show_cursor(False)
    t.gen_text("\x1b[91mZOV OS v1.4.8.8 (ARM64)\x1b[0m", 1, count=5)
    t.gen_text("login: ", 3, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("Gr00ss", 3, contin=True)
    t.gen_text("", 4, count=5)
    t.toggle_show_cursor(False)
    t.gen_text("password: ", 4, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("*********", 4, contin=True)
    t.toggle_show_cursor(False)
    time_now = datetime.now(ZoneInfo("UTC")).strftime(
        "%a %b %d %I:%M:%S %p %Z %Y"
    )
    t.gen_text(f"Last login: {time_now} on tty1", 6)

    t.gen_text("\x1b[31mgr00ss\x1b[97m@\x1b[91mwagner\x1b[0m ~> ", 7, count=5)
    prompt_col = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mclea", 7, contin=True)
    t.delete_row(7, prompt_col)  # simulate syntax highlighting
    t.gen_text("\x1b[92mclear\x1b[0m", 7, count=3, contin=True)

    try:
        ignore_repos = []
        git_user_details = gifos.utils.fetch_github_stats("Gr00ss", ignore_repos)
    except (ZeroDivisionError, Exception) as e:
        print(f"Warning: Could not fetch stats ({e}), using mock data")
        
        class MockStats:
            def __init__(self):
                self.user_rank = type('obj', (object,), {'level': 'S+'})()
                self.total_stargazers = 0
                self.total_commits_last_year = 100
                self.total_pull_requests_made = 0
                self.total_repo_contributions = 12
                self.languages_sorted = [('Python', 1), ('JavaScript', 1), ('Shell', 1)]
        
        git_user_details = MockStats()
    
    t.clear_frame()
    top_languages = [lang[0] for lang in git_user_details.languages_sorted]
    user_details_lines = f"""
    \x1b[30;101mGr00ss@GitHub\x1b[0m
    --------------
    \x1b[31mOS:     \x1b[97mARCH Linux, Fedora Linux\x1b[0m
    \x1b[31mHost:   \x1b[97mTry hard  Developer\x1b[0m
    \x1b[31mIDE:    \x1b[97mVSCode, VIM, NEOVIM\x1b[0m
    
    \x1b[30;101mGitHub Stats:\x1b[0m
    --------------
    \x1b[31mUser Rating: \x1b[97m{git_user_details.user_rank.level}\x1b[0m
    \x1b[31mTotal Stars Earned: \x1b[97m{git_user_details.total_stargazers}\x1b[0m
    \x1b[31mTotal Commits ({int(year_now) - 1}): \x1b[97m{git_user_details.total_commits_last_year}\x1b[0m
    \x1b[31mTotal PRs: \x1b[97m{git_user_details.total_pull_requests_made}\x1b[0m
    \x1b[31mTotal Contributions: \x1b[97m{git_user_details.total_repo_contributions}\x1b[0m
    \x1b[31mTop Languages: \x1b[97m{', '.join(top_languages[:5])}\x1b[0m
    """
    t.gen_text("\x1b[31mgr00ss\x1b[97m@\x1b[91mwagner\x1b[0m ~> ", 1)
    prompt_col = t.curr_col
    first_command_row = 1  # Сохраняем позицию первой команды
    t.clone_frame(10)
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mneofetch.s", 1, contin=True)
    t.delete_row(1, prompt_col)
    t.gen_text("\x1b[92mneofetch.sh\x1b[0m", 1, contin=True)
    t.gen_typing_text(" -u Gr00ss", 1, contin=True)

    # Сохраняем текущее количество фреймов (включая все предыдущие)
    existing_frames_before = len([f for f in os.listdir("frames") if f.startswith("frame_") and f.endswith(".png")]) if os.path.exists("frames") else 0
    print(f"DEBUG: existing_frames_before = {existing_frames_before}")
    
    t.toggle_show_cursor(True)
    t.gen_text(user_details_lines, 2, 35, count=5, contin=True)
    
    # Фиксируем строку для комментариев, чтобы не сдвигать верхние строки
    comment_row = t.curr_row
    
    t.gen_text("\x1b[31mgr00ss\x1b[97m@\x1b[91mwagner\x1b[0m ~> ", comment_row)
    t.gen_typing_text(
        "\x1b[1;97m# «Это не конец - это только начало самой большой работы в мире,\x1b[0m",
        comment_row,
        contin=True,
    )
    t.gen_text("\x1b[31mgr00ss\x1b[97m@\x1b[91mwagner\x1b[0m ~> ", comment_row + 1)
    t.gen_typing_text(
        "\x1b[1;97m# которая будет проведена очень скоро. Ну и… Welcome to hell!» \x1b[0m",
        comment_row + 1,
        contin=True,
    )








    
    # t.save_frame("fetch_details.png")
    t.gen_text("", t.curr_row, count=120, contin=True)

    # Вставка изображения boretskiy.jpg в фреймы
    from PIL import Image
    import glob
    import re
    
    # Загружаем изображение
    try:
        portrait = Image.open("resourses/boretskiy.jpg").convert('RGBA')
        # Изменяем размер, чтобы поместилось в красную рамку (примерно 290x300 пикселей)
        #portrait.thumbnail((300, 300), Image.Resampling.LANCZOS)
        portrait = portrait.resize((290, 300), Image.Resampling.LANCZOS)
        
        # Получаем список всех фреймов и сортируем их
        frame_files = sorted(glob.glob("frames/frame_*.png"), key=lambda x: int(re.search(r'frame_(\d+)', x).group(1)))
        
        # Вставляем изображение только в фреймы начиная с existing_frames_before + 1
        inserted_count = 0
        for frame_path in frame_files:
            frame_num = int(re.search(r'frame_(\d+)', frame_path).group(1))
            if frame_num > existing_frames_before:
                frame = Image.open(frame_path).convert('RGBA')
                position = (15, 43)  # (x, y) координаты
                frame.paste(portrait, position, portrait)
                # Конвертируем обратно в RGB для совместимости с GIF
                frame = frame.convert('RGB')
                frame.save(frame_path)
                inserted_count += 1
        print(f"INFO: Image inserted into {inserted_count} frames (starting from frame {existing_frames_before + 1}), total frames: {len(frame_files)}")
    except Exception as e:
        print(f"Warning: Could not insert image ({e})")

    # Создаем GIF с помощью FFmpeg в два этапа для корректной обработки всех кадров
    import subprocess
    
    # Сначала генерируем палитру из ВСЕХ кадров
    palette_result = subprocess.run(
        [
            'ffmpeg', '-y', '-framerate', '15', '-start_number', '1', 
            '-i', 'frames/frame_%d.png', '-vf', 'palettegen=max_colors=256',
            'palette.png'
        ],
        capture_output=True,
        text=True
    )
    
    if palette_result.returncode != 0:
        print(f"ERROR: Palette generation failed: {palette_result.stderr}")
    else:
        # Затем используем эту палитру для создания GIF
        result = subprocess.run(
            [
                'ffmpeg', '-y', '-framerate', '15', '-start_number', '1', 
                '-i', 'frames/frame_%d.png', '-i', 'palette.png',
                '-lavfi', 'paletteuse=dither=bayer',
                'output.gif'
            ],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("INFO: GIF successfully created with FFmpeg")
        else:
            print(f"ERROR: FFmpeg failed: {result.stderr}")


if __name__ == "__main__":
    main()
