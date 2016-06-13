#!/usr/bin/env python

from pprint import pprint

def main():

    print "List comprehensions"

    a = range(10)
    b = []
    # for x in a:
    #     b.append(x**2)
    b = [x**2 for x in a]
    print "comprehensive square"
    print(b)
    # for x in a:
    #     if x%2 == 0:
    #         b.append(x**2)
    b = [x**2 for x in a if x%2 == 0]
    print "comprehensive square of evens"
    print(b)

    print "Sets"
    b = range(7,20)
    a.append(0)
    a.append(1)
    a.append(100)
    a.append('silly string')
    a_set = set(a)
    b_set = set(b)
    print "Union"
    print(a_set | b_set)
    print "A not in B"
    print(a_set - b_set)
    print "B not in A"
    print(b_set - a_set)
    print "Intersect of A and B"
    print(a_set & b_set)
    print "Superset"
    superset = a_set 
    superset |= b_set
    print(superset)
    
    print "Lambda Lambda Lambda"
    a = range(1,10)
    # def a_square(x):
    #    return x**2
    f = lambda x: x**2
    print "multi-variable lambda using 1 and 2"
    g = lambda x,y: x+y
    print g(1,2)
    print "Map/filter/reduce"
    # for i in a:
    #    f(i)
    print "square the set using map and lambda"
    # can also use def
    # def a_sq(x):
    #     return x**2
    # map(a_sq,a)
    pprint(map(f,a))
    print "remove out all the odd numbers using filter"
    # def even(x):
    #     if x%2 == 0:
    #         return True
    #     else:
    #         return False
    #
    # Could also do a comprehension
    # pprint([x for x in a if x%2 == 0]
    pprint(filter(lambda x: x%2 == 0, a))
    print "Reduce"
    # def a_sum(x,y):
    #     return x+y
    print "prints sum of all numbers in a"
    print(reduce(lambda x, y: x+y,a))

if __name__ == "__main__":
    main()
