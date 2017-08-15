#! /usr/bin/python3.5

import sys
import tty
import termios

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
    pass

def call(arg):
    pass

def jmp(arg):
    pass

def jmpz(arg):
    pass

def jmpneg(arg):
    pass

def ret():
    pass

def end():
    pass

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


Stack = []
Heap = {}

Instructions = {
    'push': push,
    'dup' : dup,
    'pop' : pop,
    'copy': copy
}


def execute(instructions):
    for ins in instructions:
        if type(ins) is tuple:
            operator = ins[0]
            operand = ins[1]
            Instructions[operator](operand)
        else:
            Instructions[ins]()
        print('after execution of {}, stack is: {}, heap is: {}'.format(ins, Stack, Heap))
        
