# system imports
import sys

# user imports
from config import *
from rpsConnection import *
from socketHelper import *
from threading import Thread
import api

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', help='Path to the config file', required=True)

    args = parser.parse_args()

    config = Config.readConfiguration(args.c)

    api.start_listening()


if __name__ == "__main__":
    main()