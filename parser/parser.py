#! /usr/bin/python3.5

from conf.conf import *
from ast import *

AST_CHOOSER = {
    STACK: StackAst,
    ARITH: ArithAst,
    HEAP : HeapAst,
    FLOW : FlowAst,
    IO   : IOAst
}

class Parser(object):
    def __init__(self):
        self.allowed_chars = [' ', '\t', '\n']
        self.ascii_values = [32, 9, 10]
        self.correspondences = {
            ' ':  'S',
            '\t': 'T',
            '\n': 'L'
        }
        self.IMP = [
            [' '],        #stack manipulation
            ['\t', ' '],  #arithmetic
            ['\t', '\t'], #heap access
            ['\n'],       #flow control
            ['\t', '\n']  #I/O
        ]
        self.mode = None

    def format(self, content):
        content = self.remove_forbidden_chars(content)
        if DEBUG:
            content = ''.join(self.correspondences[c] for c in content)
        return content
    
    def remove_forbidden_chars(self, content):
        return ''.join(c for c in content if c in self.allowed_chars)

    def parse(self):
        current_ast = None
        index = len(content)
        while True:
            c = content[index]
            if self.mode is None:
                if c == ' ':
                    self.mode = STACK
                elif c == '\n':
                    self.mode = FLOW
                elif c == '\t':
                    c2 = content[index + 1]
                    if c2 == ' ':
                        self.mode = ARITH
                    elif c2 == '\t':
                        self.mode = HEAP
                    elif c2 == '\n':
                        self.mode = IO
                    else:
                        raise Exception('Mode error: not recognized')
                    index += 1
                else:
                    raise Exception('Mode error: not recognized')
                index += 1
                current_ast = AST_CHOOSER[self.mode]
            else:
                pass

if __name__ == "__main__":
    filename = 'examples/wrong_chars_push_4.ws'
    p = Parser()
    c = open(filename, 'r').read()
    print(c)
