from main import FILE_PATH


def get():
    with open(FILE_PATH, 'r') as file:
        content = file.read()
        print(content)

