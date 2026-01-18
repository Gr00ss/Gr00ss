from datetime import datetime
import os
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

load_dotenv()
if os.getenv('GITHUB_TOKEN'):
    os.environ['GITHUB_TOKEN'] = os.getenv('GITHUB_TOKEN')

import gifos

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_FILE_LOGO = os.path.join(BASE_DIR, "fonts", "vtks-blocketo.regular.ttf")
FONT_FILE_BITMAP = os.path.join(BASE_DIR, "fonts", "gohufont-uni-14.pil")
FONT_FILE_TRUETYPE = os.path.join(BASE_DIR, "fonts", "IosevkaTermNerdFont-Bold.ttf")
FONT_FILE_MONA = os.path.join(BASE_DIR, "fonts", "Inversionz.otf")

def fetch_stats_safe(username):
    """Безопасное получение статистики без merged PR percentage"""
    import requests
    
    token = os.getenv('GITHUB_TOKEN')
    headers = {'Authorization': f'Bearer {token}'}
    
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          totalCommitContributions
          restrictedContributionsCount
        }
        repositories(first: 100, ownerAffiliations: OWNER, orderBy: {field: STARGAZERS, direction: DESC}) {
          totalCount
          nodes {
            stargazerCount
            primaryLanguage {
              name
            }
          }
        }
        pullRequests {
          totalCount
        }
      }
    }
    """
    
    response = requests.post(
        'https://api.github.com/graphql',
        json={'query': query, 'variables': {'login': username}},
        headers=headers
    )
    
    data = response.json()['data']['user']
    
    class Stats:
        def __init__(self):
            self.total_stargazers = sum(repo['stargazerCount'] for repo in data['repositories']['nodes'])
            self.total_commits_last_year = data['contributionsCollection']['totalCommitContributions']
            self.total_pull_requests_made = data['pullRequests']['totalCount']
            self.total_repo_contributions = data['repositories']['totalCount']
            
            languages = {}
            for repo in data['repositories']['nodes']:
                if repo['primaryLanguage']:
                    lang = repo['primaryLanguage']['name']
                    languages[lang] = languages.get(lang, 0) + 1
            
            self.languages_sorted = sorted(languages.items(), key=lambda x: x[1], reverse=True)
            
            self.user_rank = type('obj', (object,), {'level': 'S+'})()
    
    return Stats()

def main():
    print("Fetching GitHub stats...")
    try:
        git_user_details = fetch_stats_safe("Gr00ss")
    except (ZeroDivisionError, Exception) as e:
        print(f"⚠️ Warning: Error fetching stats: {e}")
        print("Using fallback GIF without stats")
        create_simple_gif()
        return
    
    print("Creating terminal...")
    t = gifos.Terminal(750, 500, 15, 15)

    t.gen_text("", 1, count=20)
    t.toggle_show_cursor(False)
    year_now = datetime.now(ZoneInfo("UTC")).strftime("%Y")
    t.gen_text("GIF_OS Modular BIOS v1.0.11", 1)
    t.gen_text(f"Copyright (C) {year_now}, \x1b[31mGr00ss Softwares Inc.\x1b[0m", 2)
    t.gen_text("\x1b[94mGitHub Profile ReadMe Terminal, Rev 1011\x1b[0m", 4)
    t.gen_text("Krypton(tm) GIFCPU - 250Hz", 6)
    t.gen_text(
        "Press \x1b[94mDEL\x1b[0m to enter SETUP, \x1b[94mESC\x1b[0m to cancel Memory Test",
        t.num_rows,
    )
    
    for i in range(0, 65653, 7168):
        t.delete_row(7)
        if i < 30000:
            t.gen_text(f"Memory Test: {i}", 7, count=2, contin=True)
        else:
            t.gen_text(f"Memory Test: {i}", 7, contin=True)
    t.delete_row(7)
    t.gen_text("Memory Test: 64KB OK", 7, count=10, contin=True)
    t.gen_text("", 11, count=10, contin=True)

    t.clear_frame()
    t.gen_text("Initiating Boot Sequence ", 1, contin=True)
    t.gen_typing_text(".....", 1, contin=True)
    t.gen_text("", 1, count=10, contin=True)
    
    t.clear_frame()
    t.clone_frame(5)
    
    t.toggle_show_cursor(False)
    t.gen_text("\x1b[93mGIF OS v1.0.11 (tty1)\x1b[0m", 1, count=5)
    t.gen_text("login: ", 3, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("Gr00ss", 3, contin=True)
    t.gen_text("", 4, count=5)
    t.toggle_show_cursor(False)
    t.gen_text("password: ", 4, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("*********", 4, contin=True)
    t.toggle_show_cursor(False)
    
    time_now = datetime.now(ZoneInfo("UTC")).strftime("%a %b %d %I:%M:%S %p %Z %Y")
    t.gen_text(f"Last login: {time_now} on tty1", 6)

    t.gen_prompt(7, count=5)
    prompt_col = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mclea", 7, contin=True)
    t.delete_row(7, prompt_col)
    t.gen_text("\x1b[92mclear\x1b[0m", 7, count=3, contin=True)

    t.clear_frame()
    top_languages = [lang[0] for lang in git_user_details.languages_sorted]
    
    user_details_lines = f"""
    \x1b[30;101mGr00ss@GitHub\x1b[0m
    --------------
    \x1b[96mOS:     \x1b[93mWindows 11, Linux\x1b[0m
    \x1b[96mHost:   \x1b[93mPassionate Developer\x1b[0m
    \x1b[96mIDE:    \x1b[93mVSCode, PyCharm\x1b[0m
    
    \x1b[30;101mGitHub Stats:\x1b[0m
    --------------
    \x1b[96mUser Rating: \x1b[93m{git_user_details.user_rank.level}\x1b[0m
    \x1b[96mTotal Stars Earned: \x1b[93m{git_user_details.total_stargazers}\x1b[0m
    \x1b[96mTotal Commits ({int(year_now) - 1}): \x1b[93m{git_user_details.total_commits_last_year}\x1b[0m
    \x1b[96mTotal PRs: \x1b[93m{git_user_details.total_pull_requests_made}\x1b[0m
    \x1b[96mTotal Contributions: \x1b[93m{git_user_details.total_repo_contributions}\x1b[0m
    \x1b[96mTop Languages: \x1b[93m{', '.join(top_languages[:5])}\x1b[0m
    """
    
    t.gen_prompt(1)
    prompt_col = t.curr_col
    t.clone_frame(10)
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mfetch.s", 1, contin=True)
    t.delete_row(1, prompt_col)
    t.gen_text("\x1b[92mfetch.sh\x1b[0m", 1, contin=True)
    t.gen_typing_text(" -u Gr00ss", 1, contin=True)

    t.toggle_show_cursor(False)
    monaLines = r"""
    \x1b[49m     \x1b[90;100m}}\x1b[49m     \x1b[90;100m}}\x1b[0m
    \x1b[49m    \x1b[90;100m}}}}\x1b[49m   \x1b[90;100m}}}}\x1b[0m
    \x1b[49m    \x1b[90;100m}}}}}\x1b[49m \x1b[90;100m}}}}}\x1b[0m
    \x1b[49m   \x1b[90;100m}}}}}}}}}}}}}\x1b[0m
    \x1b[49m   \x1b[90;100m}}}}}}}}}}}}}}\x1b[0m
    \x1b[49m   \x1b[90;100m}}\x1b[37;47m}}}}}}}\x1b[90;100m}}}}}\x1b[0m
    \x1b[49m  \x1b[90;100m}}\x1b[37;47m}}}}}}}}}}\x1b[90;100m}}}\x1b[0m
    \x1b[49m  \x1b[90;100m}}\x1b[37;47m}\x1b[90;100m}\x1b[37;47m}}}}}\x1b[90;100m}\x1b[37;47m}}\x1b[90;100m}}}}\x1b[0m
    \x1b[49m  \x1b[90;100m}\x1b[37;47m}}\x1b[90;100m}\x1b[37;47m}}}}}\x1b[90;100m}\x1b[37;47m}}}\x1b[90;100m}}}\x1b[0m
    \x1b[90;100m}}}\x1b[37;47m}}}}\x1b[90;100m}}}\x1b[37;47m}}}}}\x1b[90;100m}}}}\x1b[0m
    \x1b[49m  \x1b[90;100m}\x1b[37;47m}}}}}\x1b[90;100m}}\x1b[37;47m}}}}}\x1b[90;100m}}}\x1b[0m
    \x1b[49m \x1b[90;100m}}\x1b[37;47m}}}}}}}}}}}}\x1b[90;100m}}}\x1b[0m
    \x1b[90;100m}\x1b[49m  \x1b[90;100m}}\x1b[37;47m}}}}}}}}\x1b[90;100m}}}\x1b[49m  \x1b[90;100m}\x1b[0m
    \x1b[49m        \x1b[90;100m}}}}}\x1b[0m
    \x1b[49m       \x1b[90;100m}}}}}}}\x1b[0m
    \x1b[49m       \x1b[90;100m}}}}}}}}\x1b[0m
    \x1b[49m      \x1b[90;100m}}}}}}}}}}\x1b[0m
    \x1b[49m     \x1b[90;100m}}}}}}}}}}}\x1b[0m
    \x1b[49m     \x1b[90;100m}}}}}}}}}}}}\x1b[0m
    \x1b[49m     \x1b[90;100m}}\x1b[49m \x1b[90;100m}}}}}}\x1b[49m \x1b[90;100m}}\x1b[0m
    \x1b[49m        \x1b[90;100m}}}}}}}\x1b[0m
    \x1b[49m         \x1b[90;100m}}}\x1b[49m \x1b[90;100m}}\x1b[0m
    """
    t.gen_text(monaLines, 10)

    t.toggle_show_cursor(True)
    t.gen_text(user_details_lines, 2, 35, count=5, contin=True)
    
    t.gen_prompt(t.curr_row)
    t.gen_typing_text(
        "\x1b[92m# Have a nice day! Thanks for visiting my profile :)",
        t.curr_row,
        contin=True,
    )
    t.gen_text("", t.curr_row, count=120, contin=True)
    
    print("🎬 Generating GIF...")
    t.set_fps(15)
    t.gen_gif()
    
    time_now = datetime.now(ZoneInfo("UTC")).strftime("%a %b %d %I:%M:%S %p %Z %Y")
    readme_file_content = rf"""<div align="justify">
<picture>
    <source media="(prefers-color-scheme: dark)" srcset="./output.gif">
    <source media="(prefers-color-scheme: light)" srcset="./output.gif">
    <img alt="GIFOS" src="output.gif">
</picture>

<sub><i>Generated automatically using [x0rzavi/github-readme-terminal](https://github.com/x0rzavi/github-readme-terminal) on {time_now}</i></sub>
</div>"""
    
    with open("README.md", "w") as f:
        f.write(readme_file_content)
        print("✅ GIF generated successfully!")
        print("✅ README.md file generated")

def create_simple_gif():
    from datetime import datetime
    from zoneinfo import ZoneInfo
    
    # Используем встроенный шрифт для fallback
    t = gifos.Terminal(750, 500, 15, 15)
    
    # BIOS экран
    t.gen_text("", 1, count=20)
    t.toggle_show_cursor(False)
    year_now = datetime.now(ZoneInfo("UTC")).strftime("%Y")
    t.gen_text("GIF_OS Modular BIOS v1.0.11", 1)
    t.gen_text(f"Copyright (C) {year_now}, \x1b[31mGr00ss Softwares Inc.\x1b[0m", 2)
    t.gen_text("\x1b[94mGitHub Profile ReadMe Terminal, Rev 1011\x1b[0m", 4)
    t.gen_text("Krypton(tm) GIFCPU - 250Hz", 6)
    t.gen_text(
        "Press \x1b[94mDEL\x1b[0m to enter SETUP, \x1b[94mESC\x1b[0m to cancel Memory Test",
        t.num_rows,
    )
    
    # Memory Test (быстрая версия)
    for i in range(0, 65653, 14336):
        t.delete_row(7)
        t.gen_text(f"Memory Test: {i}", 7, contin=True)
    t.delete_row(7)
    t.gen_text("Memory Test: 64KB OK", 7, count=10, contin=True)
    
    t.clear_frame()
    t.gen_text("Initiating Boot Sequence ", 1, contin=True)
    t.gen_typing_text(".....", 1, contin=True)
    t.gen_text("", 2, count=10, contin=True)
    
    t.clear_frame()
    t.toggle_show_cursor(False)
    t.gen_text("\x1b[93mGIF OS v1.0.11 (tty1)\x1b[0m", 1, count=5)
    t.gen_text("login: ", 3, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("Gr00ss", 3, contin=True)
    t.gen_text("", 4, count=5)
    t.toggle_show_cursor(False)
    t.gen_text("password: ", 4, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("*********", 4, contin=True)
    t.toggle_show_cursor(False)
    
    time_now = datetime.now(ZoneInfo("UTC")).strftime("%a %b %d %I:%M:%S %p %Z %Y")
    t.gen_text(f"Last login: {time_now} on tty1", 6, count=10)
    
    t.gen_prompt(8, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[92m# GitHub stats will be available soon!", 8, contin=True)
    t.gen_text("", 9, count=120, contin=True)
    
    print("🎬 Generating fallback GIF...")
    t.set_fps(15)
    t.gen_gif()
    print("✅ GIF generated successfully: output.gif")

if __name__ == "__main__":
    main()
