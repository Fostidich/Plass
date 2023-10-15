import sys

from src.get.get import get

if len(sys.argv) == 1:
    print("no arguments")
elif sys.argv[1] == "get":
    get()
else:
    print("unknown argument")
