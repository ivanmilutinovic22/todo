#!/usr/bin/env python3

import curses
import os
import json
from enum import Enum
from datetime import datetime

class Status(Enum):
    ABANDONED = 0
    NOT_DONE = 1
    IN_PROGRESS = 2
    DONE = 3

status_symbol = ['X', '-', '>', 'O']
# Define global variables
tasks = []
current_task_index = 0

def default_curses(stdscr):
    curses.curs_set(0)
    curses.noecho()
    stdscr.attron(curses.color_pair(1))

def load_tasks():
    with open("tasks.json", "r") as file:
        tasks = json.load(file)
    return tasks

def add_task(stdscr):
    stdscr.clear()

    h, w = stdscr.getmaxyx()

    stdscr.attron(curses.color_pair(2))
    text = "ADD TASK"
    for _ in range(w // 2 - len(text) // 2):
        stdscr.addch('-')
    stdscr.addstr(0, w // 2 - len(text) // 2, text)
    for _ in range(w // 2 + len(text) // 2 + len(text) % 2, w):
        stdscr.addch('-')
    stdscr.addch('\n')

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("Title:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addch(" ")
    stdscr.refresh()

    task_title = ""
    curses.echo()
    curses.curs_set(2)
    task_title = stdscr.getstr().decode('utf-8')

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("Description:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addch(" ")
    stdscr.refresh()

    task_description = ""
    curses.echo()
    task_description = stdscr.getstr().decode('utf-8')

    tasks.append({'title' : task_title,
                  'description' : task_description,
                  'status' : Status.NOT_DONE.value,
                  'created_at' : datetime.now().strftime("%d-%m-%Y %H:%M:%S")})

    default_curses(stdscr)

def save_tasks():
    global tasks
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

def update_task(stdscr):
    global current_task_index

    stdscr.clear();

    h, w = stdscr.getmaxyx()

    stdscr.attron(curses.color_pair(2))
    text = "UPDATE TASK"
    for _ in range(w // 2 - len(text) // 2):
        stdscr.addch('-')
    stdscr.addstr(0, w // 2 - len(text) // 2, text)
    for _ in range(w // 2 + len(text) // 2 + len(text) % 2, w):
        stdscr.addch('-')
    stdscr.addch('\n')

    stdscr.addstr(f"{tasks[current_task_index]['title']}\n\n")

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("New title:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addch(" ")
    stdscr.refresh()

    curses.echo()
    curses.curs_set(2)
    new_title = stdscr.getstr().decode('utf-8')
    if new_title != "":
        tasks[current_task_index]['title'] = new_title

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("New description:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addch(" ")

    curses.echo()
    new_description = stdscr.getstr().decode('utf-8')
    if new_description != "":
        tasks[current_task_index]['description'] = new_description
        
    default_curses(stdscr)

def delete_task(stdscr):
    global tasks, current_task_index

    stdscr.clear()

    h, w = stdscr.getmaxyx()

    stdscr.attron(curses.color_pair(2))
    text = "DELETE TASK"
    for _ in range(w // 2 - len(text) // 2):
        stdscr.addch('-')
    stdscr.addstr(0, w // 2 - len(text) // 2, text)
    for _ in range(w // 2 + len(text) // 2 + len(text) % 2, w):
        stdscr.addch('-')
    stdscr.addch('\n')

    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(f"Are you sure you want to delete task: {tasks[current_task_index]['title']}\n")
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(f"(y)es (n)o:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addch(" ")
    stdscr.refresh()

    curses.echo()
    curses.curs_set(2)
    yes_no = stdscr.getch()
    
    if yes_no == ord('y'):
        del tasks[current_task_index]

    default_curses(stdscr)

def draw_screen(stdscr):
    global current_task_index

    h, w = stdscr.getmaxyx()
    curses.noecho()
    stdscr.clear();

    stdscr.attron(curses.color_pair(2))
    text = "TODO TOOL"
    for _ in range(w // 2 - len(text) // 2):
        stdscr.addch('-')
    stdscr.addstr(0, w // 2 - len(text) // 2, text)
    for _ in range(w // 2 + len(text) // 2 + len(text) % 2, w):
        stdscr.addch('-')
    stdscr.addch('\n')
    
    stdscr.attron(curses.color_pair(1))
    for index, task in enumerate(tasks):
        if index == current_task_index:
            stdscr.addstr(f"  [{status_symbol[task['status']]}]  {task['title']}\n", curses.color_pair(2))
        else:
            stdscr.addstr(f"  [{status_symbol[task['status']]}]  {task['title']}\n")

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(h-1, 0, "(q)-quit (a)-add (d)-delete (TAB)-change status (s)-sort")
    stdscr.refresh()

    default_curses(stdscr)

def draw_task_screen(stdscr):
    global tasks, current_task_index

    task = tasks[current_task_index]

    h, w = stdscr.getmaxyx()

    curses.noecho()
    stdscr.clear()

    stdscr.attron(curses.color_pair(2))
    text = "TASK INFO"
    for _ in range(w // 2 - len(text) // 2):
        stdscr.addch('-')
    stdscr.addstr(0, w // 2 - len(text) // 2, text)
    for _ in range(w // 2 + len(text) // 2 + len(text) % 2, w):
        stdscr.addch('-')
    stdscr.addch('\n')

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("Title:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(f" {task['title']}\n")
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("Description:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(f" {task['description']}\n")
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("Status:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(f" {Status(task['status']).name}\n")
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("Added:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(f" {task['created_at']}\n")

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(h-1, 0, "(b)-back (u)-update (d)-delete")
    stdscr.refresh()
    
    default_curses(stdscr)

def main(stdscr):
    global tasks, current_task_index

    curses.start_color()
    curses.init_color(1, 156, 156, 156)     # background color
    curses.init_color(2, 921, 858, 698)     # foregruond color
    curses.init_color(3, 980, 741, 184)     # yellow color
    curses.init_pair(1, 2, curses.COLOR_BLACK)
    curses.init_pair(2, 1, 3)

    # Initialize the curses window
    curses.curs_set(0)  # Hide the cursor
    tasks = load_tasks()  # Load existing tasks from a file
    tasks = sorted(tasks, key = lambda x: x['status'], reverse = True)

    stdscr.attron(curses.color_pair(1))

    # Initial screen draw
    draw_screen(stdscr)

    while True:

        # Wait for user input
        key = stdscr.getch()  # Get the user's key press

        # Handle key press events
        if key == ord('q'):  # Quit the program
            save_tasks()
            break
        elif key == ord('a'):
            add_task(stdscr)
            draw_screen(stdscr)
            draw_screen(stdscr)
        elif key == ord('\t'):
            tasks[current_task_index]['status'] =  (tasks[current_task_index]['status'] + 1) % 4
            draw_screen(stdscr)
        elif key == ord('d'):
            delete_task(stdscr);
            current_task_index = 0
            draw_screen(stdscr)
        elif key == ord('s'):
            tasks = sorted(tasks, key = lambda x: x['status'], reverse = True)
            current_task_index = 0
            draw_screen(stdscr)
        elif key == ord('k'):
            if current_task_index > 0:
                current_task_index -= 1
                draw_screen(stdscr)
        elif key == ord('j'):
            if current_task_index < len(tasks) - 1:
                current_task_index += 1
                draw_screen(stdscr)
        elif key == ord('\n'):
            draw_task_screen(stdscr)
            while True:
                key = stdscr.getch()
                if key == ord('b'):
                    break
                elif key == ord('u'):
                    update_task(stdscr)
                    draw_task_screen(stdscr)
                elif key == ord('d'):
                    delete_task(stdscr);
                    break
            current_task_index = 0
            draw_screen(stdscr)


# Start the curses application
if __name__ == "__main__":
    curses.wrapper(main)

