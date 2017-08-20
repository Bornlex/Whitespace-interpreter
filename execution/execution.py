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
    Stack.append(Stack[-1])

def copy(arg):
    if arg >= len(Stack):
        raise Exception('Stack is smaller than index to copy')
    Stack.append(Stack[-(arg - 1)])

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
    global Stack
    if arg >= len(Stack):
        Stack = [Stack[-1]]
    top = Stack[-1]
    Stack = Stack[:-(arg + 1)]
    Stack.append(top)

### !STACK FUNCTIONS ###
### ARITH FUNCTIONS ###

def add():
    if len(Stack) < 2:
        raise Exception('Stack is too small (< 2), cannot add')
    Stack[-2] = Stack[-2] + Stack[-1]
    pop()

def sub():
    if len(Stack) < 2:
        raise Exception('Stack is too small (< 2), cannot sub')
    Stack[-2] = Stack[-2] - Stack[-1]
    pop()

def mul():
    if len(Stack) < 2:
        raise Exception('Stack is too small (< 2), cannot mul')
    Stack[-2] = Stack[-2] * Stack[-1]
    pop()

def div():
    if len(Stack) < 2:
        raise Exception('Stack is too small (< 2), cannot div')
    Stack[-2] = int(Stack[-2] / Stack[-1])
    pop()

def mod():
    if len(Stack) < 2:
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
    Labels[arg] = eip + 1

def call(arg):
    index_routine = Routines[arg]
    global eip
    eip = index_routine

def jmp(arg):
    if arg is None:
        raise Exception('Label is undefined')
    global eip
    eip = Labels[arg]

def jmpz(arg):
    global eip
    global condition
    if arg is None:
        raise Exception('Label is undefined')
    if Stack[-1] == 0:
        eip = Labels[arg]
        condition = True
    else:
        condition = False
    pop()

def jmpneg(arg):
    global eip
    global condition
    if arg is None:
        raise Exception('Label is undefined')
    if Stack[-1] < 0:
        eip = Labels[arg]
        condition = True
    else:
        condition = False
    pop()

def ret():
    global eip
    eip = caller

def end():
    global finished
    finished = True

### !FLOW FUNCTIONS ###
### IO FUNCTIONS ###

def outc():
    if len(Stack) == 0:
        raise Exception('Stack is empty: cannot print char')
    sys.stdout.write(chr(Stack[-1]))
    pop()

def outi():
    if len(Stack) == 0:
        raise Exception('Stack is empty: cannot print int')
    sys.stdout.write(str(Stack[-1]))
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
#boolean to know if the conditional instruction like jmp, jmpz etc
#was true or not (i.e.: Stack [0], ins = jmpz => this context is going
# to make the execution jump because jmpz is True, so condition = True)
condition = False

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



def debug_infos(instructions):
    print('==============================')
    print('Debug info:')
    print('\tStack:    {}'.format(Stack))
    print('\tHeap:     {}'.format(Heap))
    print('\tLabels:   {}'.format(Labels))
    print('\tRoutines: {}'.format(Routines))
    print('\teip:      {} ({})'.format(eip, instructions[eip]))
    print('\tcaller:   {}'.format(caller))
    print('\tfinished: {}'.format(finished))
    print('==============================')

def function_call(function_name):
    if function_name not in Routines:
        raise Exception('Function {} not defined'.format(function_name))
    global caller
    caller = eip + 1

#this function is needed because in case of a label instruction, eip
#is set to label index + 1, but eip is also incremented at the end
#of the loop
def update_eip(ins):
    global eip
    if type(ins) is tuple:
        if ins[0] == 'jmp' or ins[0] == 'jmpz' or ins[0] == 'jmpneg':
            if condition:
                return
            eip += 1
            return
        else:
            eip += 1
            return
    eip += 1

def execute(instructions):
    while eip < len(instructions):
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
            debug_infos(instructions)
        update_eip(ins)
        if finished:
            return
        
if __name__ == '__main__':
    DEBUG = True
