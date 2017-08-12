#! /usr/bin/python3.5

### IMPORTS ###

import sys
import os

from parser.parser import *
from conf.conf import *

### !IMPORTS ###

### CONSTANTS ###

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

examples_dir_name = 'examples/'
tests_dir_name = 'tests/'

files = {
    'wrong_chars_push_4.ws',
    'push_4.ws'
}

### !CONSTANTS ###

### PARSER ###

p = Parser()

### !PARSER ###


if __name__ == '__main__':
    print(bcolors.BOLD + 'Testing [PARSER]' + bcolors.ENDC)
    for f in files:
        name = examples_dir_name + f
        tname = tests_dir_name + f
        content = open(name, 'r').read()
        example_result = p.format(content)
        expected_content = open(tname, 'r').read()[:-1]
        if example_result == expected_content:
            print('[{}OK{}] test {} passed'.format(bcolors.OKGREEN, bcolors.ENDC, name))
        else:
            print('[{}KO{}] test {} failed'.format(bcolors.FAIL, bcolors.ENDC, name))
            rname = tests_dir_name + 'results/' + f.split('.')[0] + '.result'
            res = open(rname, 'w+')
            res.write('expected:\n')
            res.write('============================\n')
            res.write(expected_content)
            res.write('\n============================\n\n\n')
            res.write('got instead:\n')
            res.write('============================\n')
            res.write(example_result)
            res.write('\n============================')
            res.close()
    print(bcolors.BOLD + 'To see what failed in tests, check /tests/results/filename.result' + bcolors.ENDC + '\n')

    #AST TESTING
    print(bcolors.BOLD + 'Testing [AST]' + bcolors.ENDC)
    ast_tests = [
        (len(StackAst.sons), 3, 'len(StackAst.sons)'),
        (len(StackAst.sons['S'].sons), 0, 'len(StackAst.sons[S].sons)'),
        (len(ArithAst.sons), 2, 'len(ArithAst.sons)'),
        (len(ArithAst.sons['S'].sons), 3, 'len(ArithAst.sons[S].sons)'),
        (len(ArithAst.sons['T'].sons), 2, 'len(ArithAst.sons[T].sons)'),
        (len(HeapAst.sons), 2, 'len(HeapAst.sons)'),
        (len(HeapAst.sons['S'].sons), 0, 'len(HeapAst.sons[S].sons)'),
        (len(FlowAst.sons), 3, 'len(FlowAst.sons)'),
        (len(FlowAst.sons['S'].sons), 3, 'len(FlowAst.sons[S].sons)'),
        (len(IOAst.sons), 2, 'len(IOAst.sons)'),
        (len(IOAst.sons['S'].sons), 2, 'len(IOAst.sons[S].sons)'),
        (StackAst.sons['S'].is_leaf, True, 'StackAst.sons[S].is_leaf'),
        (StackAst.sons['S'].wil_representation, 'push', 'StackAst.sons[S].wil_representation'),
        (ArithAst.sons['S'].is_leaf, False, 'ArithAst.sons[S].is_leaf'),
        (ArithAst.sons['S'].sons['S'].wil_representation, 'add', 'ArithAst.sons[S].wil_representation'),
        (HeapAst.sons['S'].is_leaf, True, 'HeapAst.sons[S].is_leaf'),
        (HeapAst.sons['T'].wil_representation, 'retri', 'HeapAst.sons[S].wil_representation'),
        (FlowAst.sons['S'].is_leaf, False, 'FLowAst.sons[S].is_leaf'),
        (FlowAst.sons['S'].sons['S'].has_param, True, 'FlowAst.sons[S].sons[S].has_param'),
        (IOAst.sons['T'].is_leaf, False, 'IOAst.sons[T].is_leaf'),
        (IOAst.sons['S'].sons['T'].wil_representation, 'outi', 'IOAst.sons[S].sons[T].wil_representation'),
    ]
    for t in ast_tests:
        if t[0] == t[1]:
            print('[{}OK{}] {}'.format(bcolors.OKGREEN, bcolors.ENDC, t[2]))
        else:
            print('[{}KO{}] {}, got: {}, expected: {}'.format(bcolors.FAIL, bcolors.ENDC, t[2], t[0], t[1]))
