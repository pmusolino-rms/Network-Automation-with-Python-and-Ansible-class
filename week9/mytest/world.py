#!/usr/bin/env python
class MyClass(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def hello(self):
        print "Hello: {} {} {}".format(self.a, self.b, self.c)

    def not_hello(self):
        print "Goodbye: {} {} {}".format(self.a, self.b, self.c)

class MyChildClass(MyClass):
    def __init__(self, a, b, c, d):
        MyClass.__init__(self,a, b, c)
        self.d = d
        
    def hello(self):
        print "New Hello: {} {} {} {}".format(self.a, self.b, self.c, self.d) 

def hello():
    print "Hello World"

def main():
    print "{} of world".format(__name__)

if __name__ == "__main__":
    main()
