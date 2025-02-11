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

class Priority(Enum):
    OPTIONAL = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

status_symbol = ['X', '-', '>', 'O']
tasks = []
current_task_index = 0
upper_index = 0;
current_index = 0;
lower_index = 0;

def show_screen_title(stdscr, text):
    h, w = stdscr.getmaxyx()

    stdscr.attron(curses.color_pair(2))
    for _ in range(w // 2 - len(text) // 2):
        stdscr.addch('-')
    stdscr.addstr(0, w // 2 - len(text) // 2, text)
    for _ in range(w // 2 + len(text) // 2 + len(text) % 2, w):
        stdscr.addch('-')
    stdscr.addch('\n')

def show_screen_options(stdscr, text):
    h, w = stdscr.getmaxyx()

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(h-1, 0, text)

def default_curses(stdscr):
    curses.curs_set(0)
    curses.noecho()
    stdscr.attron(curses.color_pair(1))

def load_tasks():
    with open("tasks.json", "r") as file:
        tasks = json.load(file)
    return tasks

def add_task(stdscr):
    global tasks

    stdscr.clear()

    show_screen_title(stdscr, "ADD TASK")

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("Category:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addch(" ")
    stdscr.refresh()

    curses.echo()
    curses.curs_set(2)
    task_category = stdscr.getstr().decode('utf-8')

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("Title:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addch(" ")
    stdscr.refresh()

    curses.echo()
    curses.curs_set(2)
    task_title = stdscr.getstr().decode('utf-8')

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("Description:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addch(" ")
    stdscr.refresh()

    curses.echo()
    task_description = stdscr.getstr().decode('utf-8')

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("Priority (0-4):")
    stdscr.attron(curses.color_pair(1))
    stdscr.addch(" ")
    stdscr.refresh()

    curses.echo()
    task_priority = stdscr.getstr().decode('utf-8')

    if task_priority > "4" or task_priority < "0":
        task_priority = "0"

    tasks.append({'category' : task_category,
                  'title' : task_title,
                  'description' : task_description,
                  'priority' : Priority(int(task_priority)).value,
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

    show_screen_title(stdscr, "UPDATE TASK")

    stdscr.addstr(f"{tasks[current_task_index]['title']}\n\n")

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("New category:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addch(" ")
    stdscr.refresh()

    curses.echo()
    curses.curs_set(2)
    new_category = stdscr.getstr().decode('utf-8')
    if new_category != "":
        tasks[current_task_index]['category'] = new_category

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("New title:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addch(" ")
    stdscr.refresh()

    curses.echo()
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

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("New priority (0-4):")
    stdscr.attron(curses.color_pair(1))
    stdscr.addch(" ")

    curses.echo()
    new_priority = stdscr.getstr().decode('utf-8')
    if new_priority != "":
        if new_priority > "4" or new_priority < "0":
            new_priority = "0"
        tasks[current_task_index]['priority'] = Priority(int(new_priority)).value
        
    default_curses(stdscr)

def delete_task(stdscr):
    global tasks, current_task_index

    stdscr.clear()

    show_screen_title(stdscr, "DELETE TASK")

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
    global current_task_index, upper_index, lower_index

    h, w = stdscr.getmaxyx()

    stdscr.clear();

    show_screen_title(stdscr, "TODO TOOL")
    
    stdscr.attron(curses.color_pair(1))
    '''curr_category = "-1"
    for index, task in enumerate(tasks):
        if curr_category != task['category']:
            curr_category = task['category']
            if curr_category == "":
                stdscr.attron(curses.color_pair(1))
                if index == 0:
                    stdscr.addstr("-------Uncategorized\n")
                else:
                    stdscr.addstr("\n-------Uncategorized\n")
            else:
                if index == 0:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(f"-------{curr_category}\n")
                else:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(f"\n-------{curr_category}\n")

        if index == current_task_index:
            stdscr.addstr(f"  [{status_symbol[task['status']]}]  {task['title']}\n", curses.color_pair(2))
        else:
            stdscr.addstr(f"  [{status_symbol[task['status']]}]  {task['title']}\n")
    '''

    task_rows = generate_task_rows().split("\n")

    for index in range(upper_index, lower_index):
        if index == current_task_index:
            stdscr.addstr(task_rows[index] + "\n", curses.color_pair(2))
        else:
            stdscr.addstr(task_rows[index] + "\n")

    show_screen_options(stdscr, f"(q)-quit (a)-add (d)-delete (TAB)-change status (s)-sort")

    stdscr.refresh()

    default_curses(stdscr)

def generate_task_rows():
    global tasks

    tasks = sorted(tasks, key = lambda x: (x['category'], len(Status) - x['status']))

    task_rows = ""
    curr_category = "-1"
    for index, task in enumerate(tasks):
        task_rows += f"  [{status_symbol[task['status']]}]  {task['title']}\n"
    return task_rows
    

def draw_task_screen(stdscr):
    global tasks, current_task_index

    task = tasks[current_task_index]


    stdscr.clear()

    show_screen_title(stdscr, "TASK INFO")

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("Category:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(f" {task['category']}\n")

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("Title:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(f" {task['title']}\n")

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("Description:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(f" {task['description']}\n")

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("Priority:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(f" {Priority(task['priority']).name}\n")

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("Status:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(f" {Status(task['status']).name}\n")

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr("Added:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(f" {task['created_at']}\n")

    show_screen_options(stdscr, "(b)-back (u)-update (d)-delete")

    stdscr.refresh()
    
    default_curses(stdscr)

def main(stdscr):
    global tasks, current_task_index, upper_index, lower_index

    curses.start_color()
    curses.init_color(1, 156, 156, 156)     # background color
    curses.init_color(2, 921, 858, 698)     # foregruond color
    curses.init_color(3, 980, 741, 184)     # yellow color
    curses.init_pair(1, 2, curses.COLOR_BLACK)
    curses.init_pair(2, 1, 3)

    tasks = load_tasks() 

    stdscr.attron(curses.color_pair(1))

    h, w = stdscr.getmaxyx()
    lower_index = min(len(tasks), h - 4)

    draw_screen(stdscr)

    while True:
        key = stdscr.getch()  

        if key == ord('q'):
            save_tasks()
            break
        elif key == ord('a'):
            add_task(stdscr)
            current_task_index = 0
            upper_index = 0
            lower_index = min(len(tasks), h - 4)
            draw_screen(stdscr)
        elif key == ord('\t'):
            tasks[current_task_index]['status'] =  (tasks[current_task_index]['status'] + 1) % 4
            draw_screen(stdscr)
        elif key == ord('d'):
            delete_task(stdscr);
            current_task_index = 0
            upper_index = 0
            lower_index = min(len(tasks), h - 4)
            draw_screen(stdscr)
        elif key == ord('s'):
            draw_screen(stdscr)
        elif key == ord('k'):
            if current_task_index > 0:
                current_task_index -= 1
                if current_task_index < upper_index:
                    upper_index = current_task_index
                    lower_index -= 1
                draw_screen(stdscr)
        elif key == ord('j'):
            if current_task_index < len(tasks) - 1:
                current_task_index += 1
                if current_task_index >= lower_index:
                    upper_index += 1
                    lower_index = current_task_index+1
                draw_screen(stdscr)
        elif key == ord('\n'):
            draw_task_screen(stdscr)
            while True:
                key = stdscr.getch()
                if key == ord('b'):
                    break
                elif key == ord('u'):
                    update_task(stdscr)
                    current_task_index = 0
                    upper_index = 0
                    lower_index = min(len(tasks), h - 4)
                    draw_task_screen(stdscr)
                elif key == ord('d'):
                    delete_task(stdscr);
                    current_task_index = 0
                    upper_index = 0
                    lower_index = min(len(tasks), h - 4)
                    break
            draw_screen(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)

