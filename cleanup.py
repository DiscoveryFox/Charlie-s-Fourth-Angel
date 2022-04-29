#!/usr/bin/python3.10
import setup
import os


def main():
    # check if the current path ends with /Charlie-s-Fourth-Angel
    if os.getcwd().split("/")[-1] == "Charlie-s-Fourth-Angel":
        setup.customize_app()


if __name__ == "__main__":
    main()
