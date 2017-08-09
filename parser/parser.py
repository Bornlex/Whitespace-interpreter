#! /usr/bin/python3.5

from conf.conf import *

class Parser(object):
    def __init__(self):
        self.allowed_chars = [' ', '\t', '\n']
        self.ascii_values = [32, 9, 10]
        self.correspondences = {
            ' ':  'S',
            '\t': 'T',
            '\n': 'L'
        }

    def format(self, content):
        content = self.remove_forbidden_chars(content)
        if DEBUG:
            content = ''.join(self.correspondences[c] for c in content)
        content = self.remove_end_of_program(content)
        return content
    
    def remove_forbidden_chars(self, content):
        return ''.join(c for c in content if c in self.allowed_chars)

    def split_by_lines(self, content):
        char = '\n'
        if DEBUG:
            char = 'L'
        return content.split(char)

    def remove_end_of_program(self, content):
        return content[:-3]


if __name__ == "__main__":
    filename = 'examples/wrong_chars_push_4.ws'
    p = Parser()
    c = open(filename, 'r').read()
    c = p.format(c)
    print(c)
