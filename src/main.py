import sys
import os
import json
from datetime import datetime


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

    def is_before(self, other):
        if self.month < other.month:
            return True
        if self.month > other.month:
            return False
        if self.day < other.day:
            return True

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
            return f"{gray}[0  \u27A4 {self.current}] {self.code:4s} {self.name}{reset}"
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
            return f"{white}[{str(i) + ' ' if i < 10 else i} \u27A4 {self.current}] {self.code:4s} {self.name}{reset}"
        orange = "\033[1;33m"
        return f"{orange}[{str(i) + ' ' if i < 10 else i} \u27A4 {self.current}] {self.code:4s} {self.name}{reset}"


def print_content(content_list):
    if len(content_list) == 0:
        print("\t[ NO COURSE FOUND ]")
    for course in content_list:
        print("\t" + repr(Course(course['name'],
                                 course['code'],
                                 Date(course['current'][0], course['current'][1]),
                                 course['lectures'])))
    global tot
    res = tot
    tot = 0
    return res


def cmd_show():
    with open(FILE_PATH, 'r') as json_file:
        content = json_file.read()
    content_list = json.loads(content)
    print()
    t = print_content(content_list)
    print(f"\nYou are a total of {t} lectures behind")


def cmd_step(code):
    with open(FILE_PATH, 'r') as json_file:
        content = json_file.read()
    content_list = json.loads(content)
    idx = -1
    for i in range(len(content_list)):
        if content_list[i]['code'] == code:
            idx = i
            break
    if idx == -1:
        print("Course provided do not exist")
        return
    course = content_list[idx]
    if len(course['lectures']) == 0:
        print("No lectures for this course")
        return
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


def cmd_back(code):
    with open(FILE_PATH, 'r') as json_file:
        content = json_file.read()
    content_list = json.loads(content)
    idx = -1
    for i in range(len(content_list)):
        if content_list[i]['code'] == code:
            idx = i
            break
    if idx == -1:
        print("Course provided do not exist")
        return
    course = content_list[idx]
    if len(course['lectures']) == 0:
        print("No lectures for this course")
        return
    curr_date = Date(course['current'][0], course['current'][1])
    course = Course(course['name'],
                    course['code'],
                    curr_date,
                    course['lectures'])
    if curr_date.day == 0:
        course.current = course.lectures[len(course.lectures) - 1]
    else:
        for i in range(len(course.lectures)):
            date = Date(course.lectures[i][0], course.lectures[i][1])
            if date.equals(curr_date):
                if i == 0:
                    print("No lecture of the course has been seen yet")
                    return
                course.current = course.lectures[i - 1]
                break
    content_list[idx]['current'] = course.current
    content = json.dumps(content_list)
    with open(FILE_PATH, 'w') as json_file:
        json_file.write(content)
    print()
    print_content(content_list)
    print(f"\nLecture of {Date(course.current[0], course.current[1])} for {code} set to be seen again")


def cmd_get(code):
    with open(FILE_PATH, 'r') as json_file:
        content = json_file.read()
    content_list = json.loads(content)
    idx = -1
    for i in range(len(content_list)):
        if content_list[i]['code'] == code:
            idx = i
            break
    if idx == -1:
        print("Course provided do not exist")
        return
    course = content_list[idx]
    if len(course['lectures']) == 0:
        print("No lectures for this course")
        return
    curr_date = Date(course['current'][0], course['current'][1])
    course = Course(course['name'],
                    course['code'],
                    curr_date,
                    course['lectures'])
    print()
    gray = "\033[1;30m"
    orange = "\033[1;33m"
    white = "\033[1;37m"
    reset = "\033[0m"
    current_date = datetime.now()
    today = Date(current_date.day, current_date.month)
    for el in course.lectures:
        date = Date(el[0], el[1])
        if curr_date.day == 0:
            print(f"{gray}\t[ {date} ]{reset}")
            continue
        if date.is_before(curr_date):
            print(f"{gray}\t[ {date} ]{reset}")
            continue
        if date.is_before_or_equals(today) and not date.is_before(curr_date):
            print(f"{orange}\t[ {date} ]{reset}")
            continue
        if not date.is_before_or_equals(today) and not date.is_before(curr_date):
            print(f"{white}\t[ {date} ]{reset}")
    print()


def cmd_add(code, date):
    temp = date.split('-')
    try:
        date = Date(int(temp[0]), int(temp[1]))
    except ValueError:
        print("Not a date")
        return
    with open(FILE_PATH, 'r') as json_file:
        content = json_file.read()
    content_list = json.loads(content)
    idx = -1
    for i in range(len(content_list)):
        if content_list[i]['code'] == code:
            idx = i
            break
    if idx == -1:
        print("Course provided do not exist")
        return
    course = content_list[idx]
    curr_date = Date(course['current'][0], course['current'][1])
    course = Course(course['name'],
                    course['code'],
                    curr_date,
                    course['lectures'])
    idx2 = 0
    found = False
    for i in range(len(course.lectures)):
        temp = Date(course.lectures[i][0], course.lectures[i][1])
        if date.equals(temp):
            print("Date is present already")
            return
        if date.is_before(temp):
            idx2 = i
            found = True
            break
    if not found:
        course.lectures.append([date.day, date.month])
    else:
        temp = course.lectures[idx2]
        course.lectures[idx2] = [date.day, date.month]
        for i in range(idx2 + 1, len(course.lectures)):
            temp2 = course.lectures[i]
            course.lectures[i] = temp
            temp = temp2
        course.lectures.append(temp)
    if course.current.day == 0:
        content_list[idx]['current'] = [date.day, date.month]
    content_list[idx]['lectures'] = course.lectures
    content = json.dumps(content_list)
    with open(FILE_PATH, 'w') as json_file:
        json_file.write(content)
    print()
    print_content(content_list)
    print(f"\nLecture of {date} added for {code}")
    global additions
    additions += 1


def cmd_remove(code, date):
    date = date.split('-')
    try:
        date = [int(date[0]), int(date[1])]
    except ValueError:
        print("Not a date")
        return
    with open(FILE_PATH, 'r') as json_file:
        content = json_file.read()
    content_list = json.loads(content)
    idx = -1
    for i in range(len(content_list)):
        if content_list[i]['code'] == code:
            idx = i
            break
    if idx == -1:
        print("Course provided do not exist")
        return
    course = content_list[idx]
    curr_date = Date(course['current'][0], course['current'][1])
    course = Course(course['name'],
                    course['code'],
                    curr_date,
                    course['lectures'])
    if Date(date[0], date[1]).equals(curr_date):
        index = course.lectures.index(date)
        if index == len(course.lectures) - 1:
            content_list[idx]['current'] = [0, 0]
        else:
            content_list[idx]['current'] = course.lectures[index + 1]
    if date in course.lectures:
        course.lectures.remove(date)
    else:
        print("Lecture date not found")
        return
    if len(course.lectures) == 0:
        content_list[idx]['current'] = [0, 1]
    content_list[idx]['lectures'] = course.lectures
    content = json.dumps(content_list)
    with open(FILE_PATH, 'w') as json_file:
        json_file.write(content)
    print()
    print_content(content_list)
    print(f"\nLecture of {Date(date[0], date[1])} removed from {code}")


def cmd_create(code, name):
    name = ''.join([' ' if char == '_' else char for char in name])
    with open(FILE_PATH, 'r') as json_file:
        content = json_file.read()
    content_list = json.loads(content)
    for c in content_list:
        if c['name'] == name or c['code'] == code:
            print("Course name or code already in use")
            return
    course = {
        'name': name,
        'code': code,
        'current': [0, 1],
        'lectures': []
    }
    content_list.append(course)
    content = json.dumps(content_list)
    with open(FILE_PATH, 'w') as json_file:
        json_file.write(content)
    print()
    print_content(content_list)
    print(f"\nCourse \"{name}\" ({code}) added")


def cmd_delete(code):
    with open(FILE_PATH, 'r') as json_file:
        content = json_file.read()
    content_list = json.loads(content)
    name = None
    for c in content_list:
        if c['code'] == code:
            name = c['name']
            content_list.remove(c)
            break
    if name is None:
        print("Course provided do not exist")
        return
    content = json.dumps(content_list)
    with open(FILE_PATH, 'w') as json_file:
        json_file.write(content)
    print()
    print_content(content_list)
    print(f"\nCourse \"{name}\" ({code}) deleted")


def cmd_import(code):
    original_stdout = sys.stdout
    from io import StringIO
    sys.stdout = StringIO()
    while True:
        try:
            line = input()
            if not line:
                break
            cmd_add(code, line)
        except EOFError:
            break
    sys.stdout = original_stdout
    print(f"{additions} dates added for {code}")


def cmd_reset(code):
    with open(FILE_PATH, 'r') as json_file:
        content = json_file.read()
    content_list = json.loads(content)
    name = None
    for c in content_list:
        if c['code'] == code:
            name = c['name']
            if c['current'] == [0, 1]:
                print("Course has no lecture to be seen")
                return
            c['current'] = c['lectures'][0]
            break
    if name is None:
        print("Course provided do not exist")
        return
    content = json.dumps(content_list)
    with open(FILE_PATH, 'w') as json_file:
        json_file.write(content)
    print()
    print_content(content_list)
    print(f"\nLectures of course \"{name}\" ({code}) now have all been set to be seen")


def cmd_finish(code):
    with open(FILE_PATH, 'r') as json_file:
        content = json_file.read()
    content_list = json.loads(content)
    name = None
    for c in content_list:
        if c['code'] == code:
            name = c['name']
            if c['current'] == [0, 0]:
                print("Course finished already")
                return
            if c['current'] == [0, 1]:
                print("Course has no lectures that could have been seen")
                return
            c['current'] = [0, 0]
            break
    if name is None:
        print("Course provided do not exist")
        return
    content = json.dumps(content_list)
    with open(FILE_PATH, 'w') as json_file:
        json_file.write(content)
    print()
    print_content(content_list)
    print(f"\nCourse \"{name}\" ({code}) set as completed")


def cmd_example():
    gray = "\033[1;30m"
    white = "\033[1;37m"
    reset = "\033[0m"
    print("Usage: use \"plass\" followed by a command and the respective arguments\n" +
          "\n" + gray +
          f"\t[5 ➤ 10-08] FAI  Fundaments of artificial intelligence\n" +
          f"\t[0 ➤ 12-11] AM2  Analisi matematica 2\n" +
          f"\t[0 ➤  --- ] LeA  Logica e algebra\n" +
          f"\t[4 ➤ 10-10] CG   Chimica generale\n" +
          reset + "\n" +
          f"\t{white}plass show \u27A4 {reset}plass show\n" +
          f"\t{white}plass step [course] \u27A4 {reset}plass step FAI\n" +
          f"\t{white}plass back [course] \u27A4 {reset}plass back FAI\n" +
          f"\t{white}plass get [course] \u27A4 {reset}plass get GC\n" +
          f"\t{white}plass add [course] [date] \u27A4 {reset}plass add LeA 20-11\n" +
          f"\t{white}plass remove [course] [date] \u27A4 {reset}plass remove LeA 20-11\n" +
          f"\t{white}plass create [course] [name] \u27A4 {reset}plass create TdS Teoria_dei_sistemi\n" +
          f"\t{white}plass delete [course] \u27A4 {reset}plass delete TdS\n" +
          f"\t{white}plass import [course] < \"dates.txt\" \u27A4 {reset}plass import CG < Documents/untitled.txt\n" +
          f"\t{white}plass reset [course] \u27A4 {reset}plass reset FAI\n" +
          f"\t{white}plass finish [course] \u27A4 {reset}plass finish FAI\n" +
          f"\t{white}plass example \u27A4 {reset}plass example\n" +
          f"\t{white}plass help \u27A4 {reset}plass help\n" +
          "\nPlease feel free to open a discussion/issue on https://github.com/Fostidich/Plass if you encounter any issues or have questions")


def cmd_help():
    white = "\033[1;37m"
    reset = "\033[0m"
    print("Usage: use \"plass\" followed by a command and the respective arguments\n\n" +
          f"\t{white}plass show \u27A4 {reset}prints all the courses info\n" +
          f"\t{white}plass step [course] \u27A4 {reset}marks the current lesson for the course as seen\n" +
          f"\t{white}plass back [course] \u27A4 {reset}marks the last seen lesson for the course as current\n" +
          f"\t{white}plass get [course] \u27A4 {reset}prints the full stack of lessons dates for the course\n" +
          f"\t{white}plass add [course] [date] \u27A4 {reset}adds the lesson date to the stack of the course\n" +
          f"\t{white}plass remove [course] [date] \u27A4 {reset}removes the lesson date from the stack of the course\n" +
          f"\t{white}plass create [course] [name] \u27A4 {reset}creates a new course\n" +
          f"\t{white}plass delete [course] \u27A4 {reset}deletes the full course\n" +
          f"\t{white}plass import [course] < \"dates.txt\" \u27A4 {reset}adds all the lectures dates to the course\n" +
          f"\t{white}plass reset [course] \u27A4 {reset}sets the current lecture date to the first of the list\n" +
          f"\t{white}plass finish [course] \u27A4 {reset}sets all the lectures as seen\n" +
          f"\t{white}plass example \u27A4 {reset}opens the view for usage examples\n" +
          f"\t{white}plass help \u27A4 {reset}opens this very view\n" +
          "\nPlease feel free to open a discussion/issue on https://github.com/Fostidich/Plass if you encounter any issues or have questions")


executable_path = os.path.dirname(sys.executable)
directory = os.path.join(executable_path, "plass-data")
if not os.path.exists(directory):
    os.makedirs(directory)
FILE_PATH = os.path.join(directory, "lectures.json")
if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, 'w') as file:
        file.write('[]')

tot = 0
additions = 0

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("No arguments provided! Use \"plass help\" to get a list of commands")
    elif sys.argv[1] == "show" and len(sys.argv) == 2:
        cmd_show()
    elif sys.argv[1] == "step" and len(sys.argv) == 3:
        cmd_step(sys.argv[2])
    elif sys.argv[1] == "back" and len(sys.argv) == 3:
        cmd_back(sys.argv[2])
    elif sys.argv[1] == "get" and len(sys.argv) == 3:
        cmd_get(sys.argv[2])
    elif sys.argv[1] == "add" and len(sys.argv) == 4:
        cmd_add(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "remove" and len(sys.argv) == 4:
        cmd_remove(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "create" and len(sys.argv) == 4:
        cmd_create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "delete" and len(sys.argv) == 3:
        cmd_delete(sys.argv[2])
    elif sys.argv[1] == "import" and len(sys.argv) == 3:
        cmd_import(sys.argv[2])
    elif sys.argv[1] == "reset" and len(sys.argv) == 3:
        cmd_reset(sys.argv[2])
    elif sys.argv[1] == "finish" and len(sys.argv) == 3:
        cmd_finish(sys.argv[2])
    elif sys.argv[1] == "example" and len(sys.argv) == 2:
        cmd_example()
    elif sys.argv[1] == "help" and len(sys.argv) == 2:
        cmd_help()
    else:
        print("Unknown argument! Use \"plass help\" to get a list of commands")
