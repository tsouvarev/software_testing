from Aspyct import Aspect
from operator import add, div, mul, sub #, pow

operations = {"(": {"priority": 0, "f": None}, 
              ")": {"priority": 1, "f": None}, 
              "+": {"priority": 2, "f": add}, 
              "-": {"priority": 2, "f": sub}, 
              "*": {"priority": 3, "f": mul}, 
              "/": {"priority": 3, "f": div}}
#                ,"**": {"priority": 4, "f": None} 4}

class AbstractTreeAddContract (Aspect):

    def atCall (self, cd):

        self.old_length = len (cd.self.tree)

    def atReturn (self, cd):

        assert len (cd.self.tree) == self.old_length + 1, "Not working method 'add' in 'AbstractTree'"

class AbstractTreePopContract (Aspect):

    def atCall (self, cd):

        self.old_length = len (cd.self.tree)

    def atReturn (self, cd):

        assert len (cd.self.tree) == self.old_length - 1, "Not working method 'pop' in 'AbstractTree'"

class AbstractTree (object):

    def __init__ (self):

        self.tree = []

    @AbstractTreeAddContract()
    def add (self, value): self.tree.append (value)

    @AbstractTreePopContract()
    def pop (self): return self.tree.pop ()

    def __len__ (self): return len (self.tree)

class Number (object):

    def __init__ (self, num):

        self.num = float (num)

    value = property (lambda self: self.num)
    __repr__ = lambda self: str (self.value)

class Operation (object):

    def __init__ (self, op):

        self.op = op
        self.priority = operations[op]["priority"]
        self.f = operations[op]["f"]

    value = property (lambda self: self.op)
    __repr__ = lambda self: str (self.value)
    eval = lambda self, *args: self.f (*[x.value for x in args])
