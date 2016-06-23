# system imports
import sys

# user imports
from config import *


def main():
    print(sys.version)
    print(Config.readConfiguration(""))
    print("abc")

if __name__ == "__main__":
    main()