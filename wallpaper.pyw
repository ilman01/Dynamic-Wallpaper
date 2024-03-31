import ctypes
import win32con
import atexit
import time

import pystray
from PIL import Image
from pystray import MenuItem as item
import threading
import os
import sys
from datetime import datetime
import shutil

import ctypes
import pythoncom
import win32gui
from win32com.shell import shell, shellcon
from typing import List



sys.path.insert(0, os.path.abspath('./wallpaper/'))
import schedule



user32 = ctypes.windll.user32

def _make_filter(class_name: str, title: str):
    def enum_windows(handle: int, h_list: list):
        if not (class_name or title):
            h_list.append(handle)
        if class_name and class_name not in win32gui.GetClassName(handle):
            return True  # continue enumeration
        if title and title not in win32gui.GetWindowText(handle):
            return True  # continue enumeration
        h_list.append(handle)
    return enum_windows

def find_window_handles(parent: int = None, window_class: str = None, title: str = None) -> List[int]:
    cb = _make_filter(window_class, title)
    try:
        handle_list = []
        if parent:
            win32gui.EnumChildWindows(parent, cb, handle_list)
        else:
            win32gui.EnumWindows(cb, handle_list)
        return handle_list
    except:
        return []

def force_refresh():
    user32.UpdatePerUserSystemParameters(1)

def enable_activedesktop():
    try:
        progman = find_window_handles(window_class='Progman')[0]
        cryptic_params = (0x52c, 0, 0, 0, 500, None)
        user32.SendMessageTimeoutW(progman, *cryptic_params)
    except IndexError as e:
        raise WindowsError('Cannot enable Active Desktop') from e

def change_wallpaper_with_fade(image_path: str, use_activedesktop: bool = True):
    if use_activedesktop:
        enable_activedesktop()
    pythoncom.CoInitialize()
    iad = pythoncom.CoCreateInstance(shell.CLSID_ActiveDesktop, None, pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IActiveDesktop)
    iad.SetWallpaper(str(image_path), 0)
    iad.ApplyChanges(shellcon.AD_APPLY_ALL)
    force_refresh()




def change_wallpaper(path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)

def get_current_wallpaper():
    ubuf = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_GETDESKWALLPAPER,len(ubuf),ubuf,0)
    return ubuf.value

def copy_file_keep_ext(src, dst):
    _, ext = os.path.splitext(src)
    dst = dst + ext
    shutil.copy2(src, dst)

def relative_to_absolute(relative_path: str) -> str:
    current_script_path = os.path.dirname(__file__)
    full_path = os.path.join(current_script_path, relative_path)
    return full_path

def exit_function():
    print("exiting...")
    print(f"Changing wallpaper back to: {og_wallpaper_path}")
    if not os.path.isfile(rf"{og_wallpaper_path}"):
        print("File doesn't exist, copy from backup...")
        shutil.copy("./wallpaper_backup/backup", og_wallpaper_path)
        print("Copied successfully.")
    change_wallpaper(rf"{og_wallpaper_path}")

    icon.stop()
    os._exit(0)
    os.system('exit')

og_wallpaper_path = str(get_current_wallpaper())
print("Original wallpaper: " + og_wallpaper_path)

# Make a copy of the current wallpaper
if os.path.isfile(rf"{og_wallpaper_path}"):
    os.makedirs("./wallpaper_backup", exist_ok=True)
    shutil.copy(og_wallpaper_path, "./wallpaper_backup/backup")
else:
    # To avoid errors, the program will not launch if the original wallpaper is not found.
    print("Original wallpaper not found... Program will abort...")
    os._exit(1)


def main():
    current_running_wallpaper = None
    while True:
        current_hour = datetime.now().hour

        # find free wallpapers here: https://windd.info/themes/free.html

        current_running_wallpaper = schedule.schedule()

        current_running_wallpaper = relative_to_absolute(current_running_wallpaper)

        if not current_running_wallpaper == get_current_wallpaper():
            change_wallpaper_with_fade(current_running_wallpaper)
            print("Changed wallpaper")
        
        print("Current Hour: " + str(current_hour), end="\r")
        time.sleep(1)


atexit.register(exit_function)

threading.Thread(target=main).start()

icon = pystray.Icon("test_icon", Image.open(r"./icon/icon.png"), "Dynamic Wallpaper", menu=pystray.Menu(item('Exit', exit_function)))
icon.run()