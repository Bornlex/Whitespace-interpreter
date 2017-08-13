#! /usr/bin/python3.5


TAB = '\t'
SPACE = ' '


def compute_number(arg):
    sign = None
    if arg[0] == SPACE:
        sign = 1
    elif arg[0] == TAB:
        sign = -1
    else:
        raise Exception('Argument error: sign is not defined {}'.format(arg))
    if len(arg) == 1:
        return 0
    binary = [1 if c == TAB else 0 for c in arg[1:]]
    return sign * (binary[0] + sum([pow(2 * b, i) for i, b in enumerate(binary[1:])]))
