import sys

from commands.add import add
from commands.complete import complete
from commands.remove import remove
from src.commands.get import get


class Course:
    def __init__(self, name, code, current, lectures):
        self.name = name
        self.code = code
        self.current = current
        self.lectures = lectures


class Date:
    def __init__(self, day, month):
        self.day = day
        self.month = month


FILE_PATH = "assets/lectures.json"

if len(sys.argv) == 1:
    print("no arguments")
elif sys.argv[1] == "get":
    get()
elif sys.argv[1] == "complete":
    complete()
elif sys.argv[1] == "add":
    add()
elif sys.argv[1] == "remove":
    remove()
else:
    print("unknown argument")
