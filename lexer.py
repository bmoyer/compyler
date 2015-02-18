#!/usr/local/bin/python

import sys    

class Symbol : str

class SymType:
    IfSym = 0
    ElseSym = 1
    EndifSym = 2
    EndSym = 3
    Ident = 4
    Number = 5
    Operator = 6

sym_table = list()

keywords = ['IF','ELSE','ENDIF','END']

idx = 0
look = ""
token = -1

def lookup(table, string):
    found = False
    i = len(table) - 1
    while(i > 0) and not found:
        if string == table[i]:
            found = True
        else:
            i -= 1
    return i


def get_lines():
    stop = ''
    s = '\n'.join(iter(raw_input, stop))
    return s

def is_add_op(s):
    return s in ['+','-']

def is_op(c):
    return c in ['+','-','*','/','<','>',':','=']

def abort(s):
    print s
    exit(0)

def expected(s):
    abort(s + ' expected')

def skip_white():
    while look.isspace():
        get_char()

def skip_comma():
    skip_white()
    if look == ',':
        get_char()
        skip_white()

def get_char():
    global idx
    global look
    look = stream[idx]
    if idx < (len(stream)-1):
        idx += 1

def get_op():
    value = ''
    if not is_op(look):
        expected('operator')
    while is_op(look):
        value += look
        get_char()
    if len(value) == 1:
        return value
    else:
        return value
        #return '?'

def initialize():
    get_char()

def match(x):
    if look == x:
        get_char()
        skip_white()
    else:
        expected('\'\'' + x + '\'\'')

def get_num():
    x = ''
    if not look.isdigit():
        expected('Integer')
    while look.isdigit():
        x += look
        get_char()
    skip_white()
    return x

def get_name():
    x = ''
    if not look.isalpha():
        expected('name')
    while look.isalnum():
        x += look.upper()
        get_char()
    skip_white()
    return x

def scan():
    if look.isalpha():
        tok = get_name()
    elif look.isdigit():
        tok = get_num()
    elif is_op(look):
        tok = get_op()
    else:
        tok = look
        get_char()
    skip_white()
    return tok

def factor():
    if look == '(':
        match('(')
        expression()
        match(')')
    elif look.isalpha():
        ident()
    else:
        print('MOVE #' + get_num() + ',D0')

def ident():
    name = get_name()
    if look == '(':
        match('(')
        match(')')
        print('BSR ' + name)
    else:
        print('MOVE ' + name + '(PC),D0')

def subtract():
    match('-')
    term()
    print('SUB (SP)+,D0')
    print('NEG D0')

def add():
    match('+')
    term()
    print('ADD (SP)+,D0')

def multiply():
    match('*')
    factor()
    print('MULS (SP)+,D0')

def divide():
    match('/')
    factor()
    print('MOVE (SP)+,D1')
    print('DIVS D1,D0')

def term():
    factor()
    while look in ['*','/']:
        print('MOVE D0,-(SP)')
        if look == '*':
            multiply()
        elif look == '/':
            divide()
        else:
            expected('MulOp')

def expression():
    if is_add_op(look):
        print('CLR D0')
    else:
        term()
    while is_add_op(look):
        print('MOVE D0,-(SP)')
        if look == '+':
            add()
        elif look == '-':
            subtract()
        else:
            expected('AddOp')

def assignment():
    name = get_name()
    match('=')
    expression()
    print('LEA ' + name + '(PC),A0')
    print('MOVE D0,(A0)')

stream = get_lines() 
initialize()
while True:
    tok = scan()
    print tok
    if tok == ';':
        break
