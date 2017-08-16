#! /usr/bin/python3.5

import sys
import tty
import termios

DEBUG = True

def getchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setno(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

### STACK FUNCTIONS ###

def push(arg):
    Stack.append(arg)

def dup():
    if len(Stack) == 0:
        raise Exception('Stack exception: nothing to duplicate')
    Stack.append(Stack[len(Stack) - 1])

def copy(arg):
    if arg >= len(Stack):
        raise Exception('Stack is smaller than index to copy')
    Stack.append(Stack[arg])

def swap():
    if len(Stack) < 2:
        raise Exception('Stack is < 2, cannot swap')
    tmp = Stack[0]
    Stack[0] = Stack[1]
    Stack[1] = tmp

def pop():
    if len(Stack) == 0:
        raise Exception('Stack is empty: cannot pop')
    Stack.pop()

def slide(arg):
    if arg > len(Stack):
        raise Exception('Stack is smaller that the number to slide')
    Stack = Stack[arg:]

### !STACK FUNCTIONS ###
### ARITH FUNCTIONS ###

def add():
    if len(Stack < 2):
        raise Exception('Stack is too small (< 2), cannot add')
    Stack[-2] = Stack[-2] + Stack[-1]
    pop()

def sub():
    if len(Stack < 2):
        raise Exception('Stack is too small (< 2), cannot sub')
    Stack[-2] = Stack[-2] - Stack[-1]
    pop()

def mul():
    if len(Stack < 2):
        raise Exception('Stack is too small (< 2), cannot mul')
    Stack[-2] = Stack[-2] * Stack[-1]
    pop()

def div():
    if len(Stack < 2):
        raise Exception('Stack is too small (< 2), cannot div')
    Stack[-2] = Stack[-2] / Stack[-1]
    pop()

def mod():
    if len(Stack < 2):
        raise Exception('Stack is too small (< 2), cannot mod')
    Stack[-2] = Stack[-2] % Stack[-1]
    pop()

### !ARITH FUNCTIONS ###
### HEAP FUNCTIONS ###

def store():
    if len(Stack) < 2:
        raise Exception('Stack does not contain enough elements to store')
    addr = Stack[-2]
    value = Stack[-1]
    Heap[addr] = value
    pop()
    pop()

def retrieve():
    if len(Stack) < 1:
        raise Exception('Stack is empty: cannot retrieve')
    addr = Stack[-1]
    Stack[-1] = Heap[addr]

### !HEAP FUNCTIONS ###
### FLOW FUNCTIONS ###

def label(arg):
    if arg is None:
        raise Exception('Label is undefined')
    if arg in Labels:
        raise Exception('This label is already registered')
    eip = Labels[arg]

def call(arg):
    index_routine = Routines[arg]
    eip = index_routine

def jmp(arg):
    if arg is None:
        raise Exception('Label is undefined')
    if arg in Labels:
        raise Exception('This label is already registered')
    eip = Labels[arg]

def jmpz(arg):
    if arg is None:
        raise Exception('Label is undefined')
    if arg in Labels:
        raise Exception('This label is already registered')
    if Stack[-1] == 0:
        eip = Labels[arg]
    pop()

def jmpneg(arg):
    if arg is None:
        raise Exception('Label is undefined')
    if arg in Labels:
        raise Exception('This label is already registered')
    if Stack[-1] < 0:
        eip = Labels[arg]
    pop()

def ret():
    eip = caller

def end():
    finished = True

### !FLOW FUNCTIONS ###
### IO FUNCTIONS ###

def outc():
    if len(Stack) == 0:
        raise Exception('Stack is empty: cannot print char')
    sys.write(chr(Stack[-1]))
    pop()

def outi():
    if len(Stack) == 0:
        raise Exception('Stack is empty: cannot print int')
    sys.write(Stack[-1])
    pop()

def inc():
    if len(Stack) == 0:
        raise Exception('No address found on the stack for readin char')
    Heap[Stack[-1]] = getchr()
    pop()

def ini():
    if len(Stack) == 0:
        raise Exception('No address found on the stack for readin int')
    Heap[Stack[-1]] = getchr()
    pop()

### !IO FUNCTIONS ###

#just the simple stack
Stack = []
#dictionary addresses -> value
Heap = {}
#dictionary values -> index in the list of instructions
Labels = {}
#dictionary names -> index
Routines = {}
#index of execution, register the index of the instruction being read
eip = 0
#index of function that called another function
caller = None
#boolean to know if we need to exit the program or not
finished = False


Instructions = {
    'push'  : push,
    'dup'   : dup,
    'pop'   : pop,
    'copy'  : copy,
    'swap'  : swap,
    'slide' : slide,
    'add'   : add,
    'sub'   : sub,
    'mul'   : mul,
    'div'   : div,
    'mod'   : mod,
    'store' : store,
    'retri' : retrieve,
    'label' : label,
    'call'  : call,
    'jmp'   : jmp,
    'jmpz'  : jmpz,
    'jmpneg': jmpneg,
    'ret'   : ret,
    'end'   : end,
    'outc'  : outc,
    'outi'  : outi,
    'inc'   : inc,
    'ini'   : ini
}


def debug_infos():
    print('==============================')
    print('Debug info:')
    print('\tStack:    {}'.format(Stack))
    print('\tHeap:     {}'.format(Heap))
    print('\tLabels:   {}'.format(Labels))
    print('\tRoutines: {}'.format(Routines))
    print('\teip:      {}'.format(eip))
    print('\tcaller:   {}'.format(caller))
    print('\tfinished: {}'.format(finished))
    print('==============================')

def function_call(function_name):
    if function_name not in Routines:
        raise Exception('Function {} not defined'.format(function_name))
    caller = eip + 1

def execute(instructions):
    for eip in range(len(instructions)):
        ins = instructions[eip]
        if type(ins) is tuple:
            operator = ins[0]
            operand = ins[1]
            if operator == 'call':
                function_call()
            Instructions[operator](operand)
        else:
            Instructions[ins]()
        if DEBUG:
            debug_infos()
        if finished:
            return
        
