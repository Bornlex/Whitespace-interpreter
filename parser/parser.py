#! /usr/bin/python3.5

from conf.conf import *
from parser.ast import *
from utils.utils import *

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

    def parse(self, content):
        current_ast = None
        stack = []
        wil_instructions = []
        index = 0
        while True:
            if index == len(content):
                self.mode = None
                return wil_instructions
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
            elif self.mode == ARGS:
                tmp_index = 0
                arg = []
                while content[index + tmp_index] != '\n':
                    arg.append(content[index + tmp_index])
                    tmp_index += 1
                wil_instructions[len(wil_instructions) - 1] = (wil_instructions[len(wil_instructions) - 1], compute_number(arg))
                index += tmp_index + 1
                stack = []
                self.mode = None
            else:
                try:
                    stack.append(self.correspondences[c])
                    node = current_ast.has_reached_leaf(stack)
                    if node[0]:
                        wil_instructions.append(node[2])
                        stack = []
                        if node[1]:
                            self.mode = ARGS
                        else:
                            self.mode = None
                except:
                    print('Something went wrong whislt parsing, exiting')
                    return
                index += 1

if __name__ == "__main__":
    pass
