#!/usr/bin/env python3

import curses
import os
import json
from enum import Enum

class Status(Enum):
    ABANDONED = 0
    NOT_DONE = 1
    IN_PROGRESS = 2
    DONE = 3

status_symbol = ['X', '-', '>', 'O']
# Define global variables
tasks = []
current_task_index = 0

def load_tasks():
    with open("tasks.json", "r") as file:
        tasks = json.load(file)
    return tasks

def add_task(stdscr):
    stdscr.clear()
    stdscr.addstr("Title: ")
    stdscr.refresh()
    task_title = ""
    curses.echo()
    task_title = stdscr.getstr().decode('utf-8')
    stdscr.addstr("Description: ")
    stdscr.refresh()
    task_description = stdscr.getstr().decode('utf-8')
    tasks.append({'title' : task_title,
                  'description' : task_description,
                  'status' : Status.NOT_DONE.value})

def save_tasks():
    global tasks
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

def update_task(stdscr):
    global current_task_index

    stdscr.clear();
    stdscr.addstr(0, 0, "---UPDATE TASK---\n")
    stdscr.addstr(f"Task: {tasks[current_task_index]['title']}\n\n")
    stdscr.addstr("New title: ")
    curses.echo()
    new_title = stdscr.getstr().decode('utf-8')
    if new_title != "":
        tasks[current_task_index]['title'] = new_title
    stdscr.addstr("New description: ")
    new_description = stdscr.getstr().decode('utf-8')
    if new_description != "":
        tasks[current_task_index]['description'] = new_description
    current_task_index = 0

def delete_task():
    global tasks, current_task_index

    del tasks[current_task_index]
    current_task_index = 0

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
            stdscr.addstr(f"[{status_symbol[task['status']]}] {task['title']}:\n\t", curses.color_pair(2))
            stdscr.addstr(f"{task['description']}\n", curses.color_pair(2))
        else:
            stdscr.addstr(f"[{status_symbol[task['status']]}] {task['title']}:\n\t")
            stdscr.addstr(f"{task['description']}\n")

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(h-1, 0, "(q)-exit (a)-add (u)-update (d)-delete (TAB)-change status (s)-sort")
    stdscr.refresh()
    

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
        elif key == ord('u'):
            update_task(stdscr)
            draw_screen(stdscr)
        elif key == ord('\t'):
            tasks[current_task_index]['status'] =  (tasks[current_task_index]['status'] + 1) % 4
            draw_screen(stdscr)
        elif key == ord('d'):
            delete_task();
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

# Start the curses application
if __name__ == "__main__":
    curses.wrapper(main)

