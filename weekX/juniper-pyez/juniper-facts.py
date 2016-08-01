#!/usr/bin/env python

from pprint import pprint
from juniper_connection import juniper_connection_setup


def main():
   
    dev = juniper_connection_setup()
    pprint(dev.facts)

if __name__ == "__main__":
    main()
