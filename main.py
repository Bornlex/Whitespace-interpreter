#! /usr/bin/python3.5

from parser.parser import *

def main():
    pass

if __name__ == '__main__':
    filename = 'examples/WIL/set_label.ws'
    p = Parser()
    c = open(filename, 'r').read()
    content = p.remove_forbidden_chars(c)
    print(p.parse(content))
