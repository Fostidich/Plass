import sys
import os
import json
from datetime import datetime

FILE_PATH = "plass-data/lectures.json"

tot = 0


class Date:
    def __init__(self, day, month):
        self.day = day
        self.month = month

    def __repr__(self):
        if self.day == 0:
            return " --- "
        day = str(self.day).zfill(2)
        month = str(self.month).zfill(2)
        return f"{day}-{month}"

    def equals(self, other):
        return self.day == other.day and self.month == other.month

    def is_before_or_equals(self, other):
        if self.month < other.month:
            return True
        if self.month > other.month:
            return False
        if self.day <= other.day:
            return True


class Course:
    def __init__(self, name, code, current, lectures):
        self.name = name
        self.code = code
        self.current = current
        self.lectures = lectures

    def __repr__(self):
        reset = "\033[0m"
        if self.current.day == 0:
            gray = "\033[1;30m"
            return f"{gray}[0 \u27A4 {self.current}] {self.code:4s} {self.name}{reset}"
        current_date = datetime.now()
        today = Date(current_date.day, current_date.month)
        i = 0
        global tot
        for lec in self.lectures:
            lec_date = Date(lec[0], lec[1])
            if lec_date.is_before_or_equals(today) and self.current.is_before_or_equals(lec_date):
                i += 1
                tot += 1
        if i == 0:
            white = "\033[1;37m"
            return f"{white}[{i} \u27A4 {self.current}] {self.code:4s} {self.name}{reset}"
        orange = "\033[1;33m"
        return f"{orange}[{i} \u27A4 {self.current}] {self.code:4s} {self.name}{reset}"


def print_content(content_list):
    for course in content_list:
        print("\t" + repr(Course(course['name'],
                                 course['code'],
                                 Date(course['current'][0], course['current'][1]),
                                 course['lectures'])))


def get():
    with open(FILE_PATH, 'r') as json_file:
        content = json_file.read()
    content_list = json.loads(content)
    print()
    print_content(content_list)
    print(f"\nYou are a total of {tot} lectures behind")


def step(code):
    with open(FILE_PATH, 'r') as json_file:
        content = json_file.read()
    content_list = json.loads(content)
    idx = -1
    for i in range(len(content_list)):
        if content_list[i]['code'] == code:
            idx = i
            break
    if idx == -1:
        print("Course provided do not exists!")
        return
    course = content_list[idx]
    curr_date = Date(course['current'][0], course['current'][1])
    if curr_date.day == 0:
        print("Course has no more lectures!")
        return
    course = Course(course['name'],
                    course['code'],
                    curr_date,
                    course['lectures'])
    for i in range(len(course.lectures)):
        date = Date(course.lectures[i][0], course.lectures[i][1])
        if date.equals(curr_date) and i == len(course.lectures) - 1:
            course.current = [0, 0]
            break
        if date.equals(curr_date):
            course.current = course.lectures[i + 1]
            break
    content_list[idx]['current'] = course.current
    content = json.dumps(content_list)
    with open(FILE_PATH, 'w') as json_file:
        json_file.write(content)
    print()
    print_content(content_list)
    print(f"\nLecture of {curr_date} for {code} completed")


def add():
    print("add function")


def remove():
    print("remove command")


directory = os.path.dirname(FILE_PATH)
if not os.path.exists(directory):
    os.makedirs(directory)
if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, 'w') as file:
        file.write('[]')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("no arguments")
    elif sys.argv[1] == "get":
        get()
    elif sys.argv[1] == "step":
        step(sys.argv[2])
    elif sys.argv[1] == "add":
        add()
    elif sys.argv[1] == "remove":
        remove()
    else:
        print("unknown argument")
