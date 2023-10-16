from typing import TextIO

from main import FILE_PATH


def open_file(path: str) -> TextIO:
    return open(FILE_PATH, 'r')
