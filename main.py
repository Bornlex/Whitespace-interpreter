#! /usr/bin/python3.5

from parser.parser import *
from execution.execution import *

def main():
    pass

if __name__ == '__main__':
    filename = 'examples/WIL/push_dup.ws'
    p = Parser()
    c = open(filename, 'r').read()
    content = p.remove_forbidden_chars(c)
    instructions = p.parse(content)
    print(instructions)
    execute(instructions)
