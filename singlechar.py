#!/usr/local/bin/python

stream = raw_input()
idx = 0
look = ""

def is_add_op(s):
    return s in ['+','-']

def abort(s):
    print s
    exit(0)

def expected(s):
    abort(s + ' expected')

def get_char():
    global idx
    global look
    look = stream[idx]
    if idx < (len(stream)-1):
        idx += 1

def initialize():
    get_char()

def match(x):
    if look == x:
        get_char()
    else:
        expected('\'\'' + x + '\'\'')

def get_num():
    try:
        int(look)
    except:
        expected('Integer')
    old_look = look
    get_char()
    return old_look

def get_name():
    if look.isalpha():
        old_look = look
        get_char()
        return old_look.upper()
    else:
        print "err " + look
        expected('Name')

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

initialize()
#expression()
assignment()
if(look != stream[-1]): expected('Newline')
