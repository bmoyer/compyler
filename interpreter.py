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

def skip_white():
    while look.isspace():
        get_char()

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
        skip_white()
    else:
        expected('\'\'' + x + '\'\'')

def get_num():
    value = 0
    try:
        int(look)
    except:
        print "look was", look
        expected('Integer')
    while look.isdigit():
        value = 10 * value + int(look) - int('0')
        get_char()
    return value 

def get_name():
    token = ''
    if look.isalpha():
        while look.isalnum():
            token = token + look.upper()
            get_char()
        skip_white()
        return token
    else:
        expected('Name')

def factor():
    if look == '(':
        print "found left paren"
        match('(')
        expr = expression()
        print "expr was ",expr
        match(')')
        return expr
    else:
        return get_num()

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
    value = factor() 
    while look in ['*','/']:
        prev_look = look
        if look == '*':
            match('*')
            value = value * factor() 
        if look == '/':
            match('/')
            value = value / factor() 
    return value

def expression():
    if is_add_op(look):
        value = 0
    else:
        value = factor()
    while is_add_op(look):
        if look == '+':
            match('+')
            n = term()
            value = value + n
            print "n was ", n
        if look == ('-'):
            match('-')
            n = term()
            value = value - n
            print "n was ", n
    return value

def assignment():
    name = get_name()
    match('=')
    expression()
    print('LEA ' + name + '(PC),A0')
    print('MOVE D0,(A0)')

initialize()
print expression()
if(look != stream[-1]): expected('Newline')
