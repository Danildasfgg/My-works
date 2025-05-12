import os
import subprocess
import keyboard
import sys
import time
import threading
import random
import win32gui
import win32con

stop_flag = False


def move_random_window(hwnd):
    try:
        screen_width = win32gui.GetSystemMetrics(0)
        screen_height = win32gui.GetSystemMetrics(1)
        x = random.randint(0, screen_width - 500)
        y = random.randint(0, screen_height - 400)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, 500, 400, 0)
    except:
        pass


def check_key_press():
    global stop_flag
    keyboard.wait('д')
    stop_flag = True


def open_notepads():
    global stop_flag
    message = "Я тоже тебя очень сильно люблю, Никушенька! Чтобы остановить нажми на первую букву моего имени (Д, если затупила)"

    keyboard_thread = threading.Thread(target=check_key_press)
    keyboard_thread.daemon = True
    keyboard_thread.start()

    with open("love_message.txt", "w", encoding="utf-8") as f:
        f.write(message)

    try:
        while not stop_flag:

            notepad = subprocess.Popen(['notepad.exe', 'love_message.txt'])

            time.sleep(0.1)
            hwnd = win32gui.FindWindow(None, "love_message.txt - Блокнот")
            if hwnd:
                move_random_window(hwnd)

    finally:

        os.system('taskkill /f /im notepad.exe')
        if os.path.exists("love_message.txt"):
            os.remove("love_message.txt")


def main():
    print("Ты меня любишь?\n1 - Нет\n2 - КОНЕЧНО")
    choice = input("> ")

    if choice == '1':
        os.system('shutdown /s /t 1')
    elif choice == '2':
        print("\nСоздаю блокноты любви...")
        open_notepads()
    else:
        print("Не понял твой ответ")


if __name__ == "__main__":
    try:
        import keyboard
        import win32gui
        import win32con
    except ImportError:
        os.system('pip install keyboard pypiwin32')

    main()