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
    print('\n\n' + bcolors.BOLD + 'To see what failed in tests, check /tests/results/filename.result' + bcolors.ENDC)
