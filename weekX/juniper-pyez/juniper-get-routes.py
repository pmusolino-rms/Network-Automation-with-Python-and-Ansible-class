#!/usr/bin/env python

from juniper_connection import juniper_connection_setup, JuniperObject


def main():
   
    dev = juniper_connection_setup()
    juniper_object = JuniperObject(dev)
    juniper_object.show_all_routes()

if __name__ == "__main__":
    main()
