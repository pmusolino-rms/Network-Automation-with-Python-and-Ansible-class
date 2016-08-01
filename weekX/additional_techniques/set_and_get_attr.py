#!/usr/bin/env python


class ANetworkDevice(object):

    def __init__(self, ip, user, passwd):
        self.ip = ip
        self.username = user
        self.password = passwd

    def show_device(self):
        print "IP: {}".format(self.ip)
        print "Username: {}".format(self.username)
        print "Password: {}".format(self.password)

    def change_password(self, newpass):
        self.password = newpass


if __name__ == "__main__":
    # if the variable is equal to the name of a function or the attribute in a class,
    # it can be referenced using get_attr
    a_var = 'ip'
    some_device = ANetworkDevice("1.1.1.2", "my_name", "password")
    some_device.show_device()
    print "prints out ip since a_var = ip"
    print getattr(some_device, a_var)
    a_var = 'username'
    print getattr(some_device, a_var)
    # setattr works by changing the vaule of a function or class field/method
    a_var = 'ip'
    setattr(some_device, a_var, '2.2.2.2')
    some_device.change_password("mynewpassword")
    some_device.show_device()
