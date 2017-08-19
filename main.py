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
    loop_instructions = [
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
    instructions = [('push', 1), ('push', 2), ('push', 3), ('slide', 2)]
    print(instructions)
    execute(instructions)
