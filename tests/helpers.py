from contextlib import contextmanager
from os import path


@contextmanager
def file_reader(filename):
    relative_filename = path.join("..", path.dirname(__file__), filename)
    file = open(relative_filename)
    try:
        yield file
    finally:
        file.close()
