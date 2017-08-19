#! /usr/bin/python3.5

import sys

from parser.parser import *
from execution.execution import *

ex = sys.modules['execution.execution']

example_filename = 'examples/WIL/push_dup.ws'

def get_loop_instructions():
    return [
        ('push', 1),
        ('label', 0),
        'dup',
        'outi',
        ('push', 1),
        'add',
        'dup',
        ('push', 5),
        'sub',
        ('jmpneg', 0),
        'end'
    ]

def main(filename):
    p = Parser()
    c = open(filename, 'r').read()
    content = p.remove_forbidden_chars(c)
    instructions = p.parse(content)
    print(instructions)
    execute(instructions)

def usage():
    print('usage: ./main.py file_to_execute.ws')

if __name__ == '__main__':
    ex.DEBUG = False
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    main(sys.argv[1])
