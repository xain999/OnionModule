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

    api_thread = Thread(target=api.start_listening, args=[config])

    api_thread.start()

    while True:
        api_thread.join(1)


if __name__ == "__main__":
    main()