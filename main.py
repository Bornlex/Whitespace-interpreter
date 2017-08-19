#! /usr/bin/python3.5

from parser.parser import *
from execution.execution import *

def get_loop_instructions():
    return loop_instructions = [
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
