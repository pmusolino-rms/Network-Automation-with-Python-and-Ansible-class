#!/usr/bin/env python

from mytest import *


def main():
    hello()
    keep_it()
    man()

    a = MyClass(10, 20, 101)
    a.hello()
    a.not_hello()

if __name__ == "__main__":
    main()
