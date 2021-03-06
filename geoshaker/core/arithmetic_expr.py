# -*- coding: utf-8 -*-

'''
File: arithmetic_expr.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: Describes and evals arithmetic expressions
'''

import operator


# ARITHMETIC CLASSES
# ------------------
class ArithmeticExpr(object):
    def eval(self, values):
        pass

    def __repr__(self):
        pass


class SymbolExpr(ArithmeticExpr):
    def __init__(self, symbol):
        self.symbol = symbol

    def eval(self, values):
        if self.symbol in values:
            return values[self.symbol]
        raise IndexError

    def __repr__(self):
        return self.symbol


class IntExpr(ArithmeticExpr):
    def __init__(self, value):
        self.value = int(value)

    def eval(self, values):
        return self.value

    def __repr__(self):
        return str(self.value)

class MixedExpr(ArithmeticExpr):
    """ Mix between int and symbols (a1b for example) """
    def __init__(self, val):
        self.elements = [val]

    def addElement(self, val):
        self.elements.append(val)

    def eval(self, values):
        return int(''.join([str(elt.eval(values)) for elt in reversed(self.elements)]))

    def __repr__(self):
        return ''.join([elt.__repr__() for elt in self.elements])

class MinusExpr(ArithmeticExpr):
    def __init__(self, expr):
        self.expr = expr

    def eval(self, values):
        return - self.expr.eval(values)

    def __repr__(self):
        return '-' + str(self.expr.__repr__())

class BinOp(ArithmeticExpr):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def eval(self, values):
        return self.op(self.left.eval(values), self.right.eval(values))

    def __repr__(self):
        return self.left.__repr__() + ' OP ' + self.right.__repr__()


# LEXER
# -----
tokens = (
    'PLUS', 'MINUS',
    'TIMES', 'DIVIDE',
    'SYMBOL', 'INT',
    'LPAREN', 'RPAREN'
)

t_PLUS   = r'\+'
t_MINUS  = r'\-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_SYMBOL = r'[a-z]'
t_INT    = r'[0-9]+'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = " \t"

def t_error(t):
    pass

# Build the lexer
import ply.lex as lex
lex.lex()


# PARSER
# ------
operators = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.div
}

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS')
)

def p_statement_expr(t):
    'statement : expression'
    t[0] = t[1]

def p_expression_binop(t):
    ''' expression : expression PLUS expression
                   | expression MINUS expression
                   | expression TIMES expression
                   | expression DIVIDE expression
    '''
    t[0] = BinOp(t[1], operators[t[2]], t[3])

def p_expression_int(t):
    'expression : INT'
    t[0] = IntExpr(t[1])

def p_expression_symbol(t):
    'expression : SYMBOL'
    t[0] = SymbolExpr(t[1])

def p_expression_mix(t):
    'expression : mix_element mix_tail'
    t[0] = t[2]
    t[0].addElement(t[1])

def p_expression_mix_tail(t):
    ''' mix_tail : mix_element
                 | mix_element mix_tail
    '''
    if len(t) == 2:
        t[0] = MixedExpr(t[1])
    else:
        t[0] = t[2]
        t[0].addElement(t[1])

def p_expression_mix_symbol(t):
    'mix_element : SYMBOL'
    t[0] = SymbolExpr(t[1])

def p_expression_mix_int(t):
    'mix_element : INT'
    t[0] = IntExpr(t[1])


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = MinusExpr(t[2])

def p_error(t):
    pass

# Build parser
import ply.yacc as yacc
yacc.yacc()

def parse_expr(str_expr):
    return yacc.parse(str_expr)

if __name__ == '__main__':
    expr_str = 'a - 1'
    values = {'a' : 3, 'b' : 2, 'c' : 4}

    expr = parse_expr(expr_str)
    if expr:
        print expr.eval(values)
