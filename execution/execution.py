#! /usr/bin/python3.5


def push(arg):
    Stack.append(arg)

def dup():
    if len(Stack) == 0:
        raise('Stack exception: nothing to duplicate')
    Stack.append(Stack[len(Stack) - 1])

Stack = []
Heap = []

Instructions = {
    'push': push,
    'dup' : dup
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
        
