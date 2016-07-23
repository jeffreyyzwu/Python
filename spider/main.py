#-*-coding=utf-8-*-
__author__ = 'jeffrey'
from xitek import xitek
from zhihu import zhihu
import importlib
import sys


def main():
    for task in [xitek(), zhihu()]:
        importlib.reload(sys)
        task.getPhoto()


if __name__ == "__main__":
    main()
