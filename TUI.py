from pyfzf import FzfPrompt
import os, subprocess

'''The TUI uses fzf to make good looking menus'''


fzf = FzfPrompt()
mpv: subprocess.Popen


def play(url):
    global mpv
    mpv = subprocess.Popen(['mpv', url, '--really-quiet', '--profile=low-latency'])
    # os.system(f"mpv {url} --really-quiet")


def prompt_user():
    return "+".join(input("Search Videos: ").split())


def prompt_videos(video_list:list) -> int:
    global fzf

    video = fzf.prompt(
        video_list,
        '--layout reverse --cycle --prompt "Select Video: "'
    )[0]

    return video_list.index(video)


def video_menu():
    global fzf

    return fzf.prompt(
        [
            'Play Again',
            'Select Another Video',
            'Quit'
        ],
        '--layout reverse --cycle --prompt "Select an Option: "'
    )[0]


def video_page(url):
    global mpv
    while True:
        action = video_menu()
        
        if action == "Play Again":
            if mpv.poll() == None: continue
            play(url)

        elif action == "Select Another Video":
            return True                             # returns True means keep looking for another video in the same list

        else:
            return False                            # returns False means end program


def app(video_list, prompt_list):
    keep_watching = True
    while keep_watching:
        idx = prompt_videos(prompt_list)
        if idx == 0: break    # 0 is for Quit

        url = f"https://youtube.com/watch?v={video_list[idx-1]['ID']}"
        play(url)

        keep_watching = video_page(url)

# example usage
if __name__ == "__main__":
    print(video_menu())
