#! /usr/bin/python2
# -*- coding: utf8 -*-

from core import Number, Operation, AbstractTree
from re import match
from Aspyct import Aspect

class CalculateContract (Aspect):

    def atCall (self, cd):

      tree = cd.args[0] 

      assert type (tree) is AbstractTree, "Not an AbstractTree in 'calculate'"

class ParseContract (Aspect):

    def atCall (self, cd):

        exp = cd.args[0]

        assert type (exp) is str, "Not an str type in 'parse'"
        assert match ("[-*/+0-9 ]+\d$", exp), "Wrong syntax"

@ParseContract()
def parse (exp):
    
    tree = AbstractTree ()

    for token in exp.strip().split (" "):

        if match ("[0-9]+", token): tree.add (Number (token))
        elif match ("[+\-*/]", token): tree.add (Operation (token))
        else: raise Exception ("Error near '%s'" % token)

    return tree

@CalculateContract()
def calculate (tree):

    num_stack = []

    while len (tree) > 0:
        
        token = tree.pop ()

        if type (token) is Number: 
            
            num_stack.append (token)

        elif type (token) is Operation: 

            op1 = num_stack.pop ()
            op2 = num_stack.pop ()
            
            num_stack.append (Number (token.eval(op1,op2))) 

    return num_stack.pop()

#parse (exp)
tree = list (reversed ([ # 5-((1+2)-1)*(1+3.2)
                        Number      ("1"), 
                        Number      ("1"), 
                        Number      ("2"),
                        Operation   ("+"), 
                        Operation   ("-"),
                        Number      ("3.2"), 
                        Number      ("1"), 
                        Operation   ("+"), 
                        Operation   ("*"), 
                        Number      ("5"), 
                        Operation   ("-")]))

st = "- + 1 2 4"
exp = "(1+2)*(3+1)-2"
print calculate (parse (st))

