import sys

if sys.version_info < (3,):
    print("Requires python3.x!")
    sys.exit(1)

from core.Controller import Controller
from core.ArgvParser import ArgvParser


class Main:
    def __init__(self):
        Controller(ArgvParser().options)


if __name__ == "__main__":
    Main()
