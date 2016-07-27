# system imports
import sys

# user imports
from config import *


def main():
    print(sys.version)
    config = Config.readConfiguration("../config.ini")
    print(config)
    print("abc")

if __name__ == "__main__":
    main()