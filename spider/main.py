#-*-coding=utf-8-*-
__author__ = 'jeffrey'
from xitek import xitek
import importlib
import sys

importlib.reload(sys)


def main():
    task = xitek()
    task.getPhoto()

if __name__ == "__main__":
    main()
