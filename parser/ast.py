#! /usr/bin/python3.5


### INSTRUCTIONS ###

# instruction: ([chars list], has parameter, "representation in WIL")

CHARS = 0
PARAM = 1
WIL   = 2

STACK_INSTRUCTIONS = [
    (['S'],      True,  'push' ),
    (['L', 'S'], False, 'dup'  ),
    (['T', 'S'], True,  'copy' ),
    (['L', 'T'], False, 'swap' ),
    (['L', 'L'], False, 'pop'  ),
    (['T', 'L'], True,  'slide')
]

ARITH_INSTRUCTIONS = [
    (['S', 'S'], False, 'add'),
    (['S', 'T'], False, 'sub'),
    (['S', 'L'], False, 'mul'),
    (['T', 'S'], False, 'div'),
    (['T', 'T'], False, 'mod')
]

HEAP_INSTRUCTIONS = [
    (['S'], False, 'store'),
    (['T'], False, 'retri')
]

FLOW_INSTRUCTIONS = [
    (['S', 'S'], True,  'label' ),
    (['S', 'T'], True,  'call'  ),
    (['S', 'L'], True,  'jmp'   ),
    (['T', 'S'], True,  'jmpz'  ),
    (['T', 'T'], True,  'jmpneg'),
    (['T', 'L'], False, 'ret'   ),
    (['L', 'L'], False, 'end'   )
]

IO_INSTRUCTIONS = [
    (['S', 'S'], False, 'outc'),
    (['S', 'T'], False, 'outi'),
    (['T', 'S'], False, 'inc' ),
    (['T', 'T'], False, 'ini' )
]

### !INSTRUCTIONS ###

class Character(object):
    def __init__(self, char):
        self.char = char
        self.sons = {
        }
        self.is_leaf = True
        self.has_param = False
        self.wil_representation = None

    def add(self, chars, has_param, wil_representation):
        if len(chars) == 0:
            self.has_param = has_param
            self.wil_representation = wil_representation
            return
        if len(self.sons) == 0:
            self.is_leaf = False
        if chars[0] not in self.sons:
            self.sons[chars[0]] = Character(chars[0])
        if len(chars) == 1:
            self.sons[chars[0]].has_param = has_param
            self.sons[chars[0]].wil_representation = wil_representation
            return
        self.sons[chars[0]].add(chars[1:], has_param, wil_representation)

    def has_reached_leaf(self, chars):
        if len(chars) == 0:
            return self.is_leaf
        if self.is_leaf:
            if len(chars) != 0:
                raise Exception('Syntax error: character {} is strange. Instruction "{}" should be over.'.format(self.char, self.wil_representation))
            return True
        return self.sons[chars[0]].has_reached_leaf(chars[1:])


class Ast(object):
    def __init__(self, instructions):
        self.sons = {
        }
        for ins in instructions:
            c = ins[CHARS][0]
            if c not in self.sons:
                self.sons[c] = Character(c)
            self.sons[c].add(ins[CHARS][1:], ins[PARAM], ins[WIL])

    def has_reached_leaf(self, chars):
        c = chars[0]
        return self.sons[c].has_reached_leaf(chars[1:])

class StackAst(Ast):
    def __init__(self):
        Ast.__init__(self, STACK_INSTRUCTIONS)

class ArithmeticAst(Ast):
    def __init__(self):
        Ast.__init__(self, ARITH_INSTRUCTIONS)

class HeapAst(Ast):
    def __init__(self):
        Ast.__init__(self, HEAP_INSTRUCTIONS)

class FlowAst(Ast):
    def __init__(self):
        Ast.__init__(self, FLOW_INSTRUCTIONS)

class IOAst(Ast):
    def __init__(self):
        Ast.__init__(self, IO_INSTRUCTIONS)

StackAst = StackAst()
ArithAst = ArithmeticAst()
HeapAst = HeapAst()
FlowAst = FlowAst()
IOAst = IOAst()

if __name__ == '__main__':
    pass
