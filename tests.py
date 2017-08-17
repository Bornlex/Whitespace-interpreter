#! /usr/bin/python3.5

### IMPORTS ###

import sys
import os

from parser.parser import *
from conf.conf import *
from execution.execution import *

ex = sys.modules['execution.execution']

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

files_txt = [
    'wrong_chars_push_4.ws',
    'push_4.ws'
]

files_wil_simples = [
    'WIL/dup.ws',
    'WIL/push_1.ws',
    'WIL/set_label.ws'
]

files_wil_medium = [
    'WIL/push_dup.ws',
    'WIL/pop_add.ws'
]

STACK_POS =    0
HEAP_POS =     1
LABELS_POS =   2
ROUTINES_POS = 3

DEBUG = False

### !CONSTANTS ###

### PARSER ###

p = Parser()

### !PARSER ###

### UTILS ###

def restore_context():
    ex.Stack = []
    ex.Heap = {}
    ex.Labels = {}
    ex.Routines = {}
    ex.eip = 0
    ex.caller = None
    ex.finished = False

def perform_test(test):
    execute(test[0])
    if ex.Stack != test[1][STACK_POS]:
        return False
    if ex.Heap != test[1][HEAP_POS]:
        return False
    if ex.Labels != test[1][LABELS_POS]:
        return False
    if ex.Routines != test[1][ROUTINES_POS]:
        return False
    return True

def compare_list(l1, l2, wil=False):
    if l1 is None and l2 is not None:
        return False
    if l2 is None and l1 is not None:
        return False
    if len(l1) != len(l2):
        return False
    if wil:
        for i in range(len(l1)):
            if type(l1[i]) is tuple:
                l1[i] = '{} {}'.format(l1[i][0], l1[i][1])
            if type(l2[i]) is tuple:
                l2[i] = '{} {}'.format(l2[i][0], l2[i][1])
    for i in range(len(l1)):
        if l1[i] != l2[i]:
            return False
    return True

### !UTILS ###


if __name__ == '__main__':
    print(bcolors.BOLD + 'Testing [PARSER]' + bcolors.ENDC)
    print(bcolors.BOLD + '[PARSER][1/3] WS -> TXT' + bcolors.ENDC)
    for f in files_txt:
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
    print('To see what failed in tests, check /tests/results/filename.result\n')
    print(bcolors.BOLD + '[PARSER][2/3] WS -> WIL EASY' + bcolors.ENDC)
    for f in files_wil_simples:
        name = examples_dir_name + f
        tname = name.replace('.ws', '.wil')
        content = open(name, 'r').read()
        tcontent = open(tname, 'r').read().split('\n')
        result = p.parse(content)
        if compare_list(result, tcontent, True):
            print('[{}OK{}] test {} passed'.format(bcolors.OKGREEN, bcolors.ENDC, name))
        else:
            print('[{}KO{}] {}, had: {}, expected: {}'.format(bcolors.FAIL, bcolors.ENDC, name, result, tcontent))
    print('')
    print(bcolors.BOLD + '[PARSER][3/3] WS -> WIL MEDIUM' + bcolors.ENDC)
    for f in files_wil_medium:
        name = examples_dir_name + f
        tname = name.replace('.ws', '.wil')
        content = open(name, 'r').read()
        tcontent = open(tname, 'r').read().split('\n')
        result = p.parse(content)
        if compare_list(result, tcontent, True):
            print('[{}OK{}] test {} passed'.format(bcolors.OKGREEN, bcolors.ENDC, name))
        else:
            print('[{}KO{}] {}, had: {}, expected: {}'.format(bcolors.FAIL, bcolors.ENDC, name, result, tcontent))

    #AST TESTING
    print('\n\n' + bcolors.BOLD + 'Testing [AST]' + bcolors.ENDC)
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

    #EXECUTION TESTING
    print('\n\n' + bcolors.BOLD + 'Testing [EXECUTION]' + bcolors.ENDC)
    execution_tests = [
        ([('push', 1), 'dup'], ([1, 1], {}, {}, {}), 'push 1, dup'),
        ([('push', 2), 'dup', 'add'], ([4], {}, {}, {}), 'push 2, dup, add')
    ]
    for t in execution_tests:
        if perform_test(t):
            print('[{}OK{}] {}'.format(bcolors.OKGREEN, bcolors.ENDC, t[2]))
        else:
            print('[{}KO{}] {}, got: ({} {} {} {}), expected: {}'.format(bcolors.FAIL, bcolors.ENDC, t[2], Stack, Heap, Labels, Routines, t[1]))
        restore_context()
