#!/usr/local/bin/python

import sys    

class Symbol : str

class SymType:
    Null = -1
    IfSym = 0
    ElseSym = 1
    EndifSym = 2
    EndSym = 3
    Ident = 4
    Number = 5
    Operator = 6

Symbols = [SymType.Null, SymType.IfSym, SymType.ElseSym, SymType.EndifSym, 
            SymType.EndSym, SymType.Ident, SymType.Number, 
            SymType.Operator]


keywords = ['NULL','IF','ELSE','ENDIF','END']

idx = 0
look = ""
token = -1
value = ''

def lookup(table, string):
    try:
        idx = keywords.index(string)
    except:
        idx = 0
    return idx
    '''
    found = False
    i = len(table) - 1
    while(i > 0) and (not found):
        if string == table[i]:
            print "FOUND TOK:"
            found = True
        else:
            i -= 1
    return i
    '''

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
    try:
        look = stream[idx]
    except:
        look = ''
    #if idx < (len(stream)-1):
    idx += 1

def get_op():
    global value
    global token
    value = ''
    if not is_op(look):
        expected('operator')
    while is_op(look):
        value += look
        get_char()
    token = SymType.Operator

def initialize():
    get_char()

def match(x):
    if look == x:
        get_char()
        skip_white()
    else:
        expected('\'\'' + x + '\'\'')

def get_num():
    global value
    global token
    value = ''
    if not look.isdigit():
        expected('Integer')
    while look.isdigit():
        value += look
        get_char()
    token = SymType.Number

def get_name():
    global value
    global token
    value = ''
    if not look.isalpha():
        expected('name')
    while look.isalnum():
        value += look.upper()
        get_char()
    k = lookup(Symbols, value)
    if k == 0:
        token = SymType.Ident
    else:
        token = Symbols[k-1]

def scan():
    global value
    global token
    if look.isalpha():
        get_name()
    elif look.isdigit():
        get_num()
    elif is_op(look):
        get_op()
    else:
        value = look
        token = SymType.Operator
        get_char()
    skip_white()

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

# get code from user input
stream = get_lines() 

initialize()
while True:
    scan()
    if token == SymType.Ident:
        print 'Ident '
    elif token == SymType.Number:
        print 'Number '
    elif token == SymType.Operator:
        print 'Operator '
    elif token == SymType.EndSym:
        break
    elif value == "END":
        break
    else:
        print 'Keyword '
    print value
