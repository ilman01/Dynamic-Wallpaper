from datetime import datetime

def schedule():
    current_hour = datetime.now().hour

    if current_hour == 5:
        current_running_wallpaper = r"./wallpaper/firewatch_1.jpg"
    if current_hour == 6:
        current_running_wallpaper = r"./wallpaper/firewatch_2.jpg"
    if 7 <= current_hour <= 8:
        current_running_wallpaper = r"./wallpaper/firewatch_3.jpg"
    if 9 <= current_hour <= 14:
        current_running_wallpaper = r"./wallpaper/firewatch_4.jpg"
    if 15 <= current_hour <= 16:
        current_running_wallpaper = r"./wallpaper/firewatch_5.jpg"
    if current_hour == 17:
        current_running_wallpaper = r"./wallpaper/firewatch_6.jpg"
    if current_hour == 18:
        current_running_wallpaper = r"./wallpaper/firewatch_7.jpg"
    if 19 <= current_hour <= 23:
        current_running_wallpaper = r"./wallpaper/firewatch_8.jpg"
    if 0 <= current_hour <= 4:
        current_running_wallpaper = r"./wallpaper/firewatch_8.jpg"

    return current_running_wallpaper