#!/usr/local/bin/python

stream = raw_input()
idx = 0
look = ""

def is_add_op(s):
    return s in ['+','-']

def is_or_op(s):
    return s in ['|','~']

def is_rel_op(s):
    return s in ['=','#','<','>']

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
    value = ''
    try:
        int(look)
    except:
        expected('Integer')

    while look.isdigit():
        value = value + look
        get_char()
    skip_white()
    return value

def is_boolean(c):
    return c.upper() in ['T','F']

def get_boolean():
    if not is_boolean(look):
        expected('boolean literal')
    boolean = look.upper() == 'T'
    get_char()
    return boolean

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
        match('(')
        expression()
        match(')')
    elif look.isalpha():
        ident()
    else:
        print('MOVE #' + get_num() + ',D0')

def signed_factor():
    if look == '+':
        get_char()
    elif look == '-':
        get_char()
        if look.isdigit():
            print 'MOVE #-' + get_num() + ',D0'
        else:
            factor()
            print 'NEG D0'
    else:
        factor()

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
    print 'MOVE (SP)+,D1'
    print 'EXS.L D0'
    print 'DIVS D1,D0'

def term():
    signed_factor()
    while look in ['*','/']:
        print('MOVE D0,-(SP)')
        if look == '*':
            multiply()
        elif look == '/':
            divide()
        else:
            expected('MulOp')

def expression():
    term()
    while is_add_op(look):
        print 'MOVE D0,-(SP)'
        old_look = look
        if old_look == '+':
            add()
        if old_look == '-':
            subtract()


def bool_expression():
    bool_term()
    while is_or_op(look):
        print 'MOVE D0,-(SP)'
        old_look = look
        if old_look == '|':
            bool_or()
            continue
        if old_look == '~':
            bool_xor()
            continue

def bool_factor():
    if is_boolean(look):
        if get_boolean():
            print 'MOVE #-1,D0'
        else:
            print 'CLR D0'
    else:
        relation()

def relation():
    expression()
    if is_rel_op(look):
        print 'MOVE D0,-(SP)'
        old_look = look
        if old_look == '=':
            equals()
        if old_look == '#':
            not_equals()
        if old_look == '<':
            less()
        if old_look == '>':
            greater()
        print 'TST D0'

def not_factor():
    if look == '!':
        match('!')
        bool_factor()
        print 'EOR #-1,D0'
    else:
        bool_factor()

def bool_term():
    not_factor()
    while look == '&':
        print 'MOVE D0,-(SP)'
        match('&')
        not_factor()
        print 'AND (SP)+,D0'

def bool_or():
    match('|')
    bool_term()
    print 'OR (SP)+,D0'

def bool_xor():
    match('~')
    bool_term()
    print 'EOR (SP)+,D0'

def equals():
    match('=')
    expression()
    print 'CMP (SP)+,D0'
    print 'SEQ D0'

def not_equals():
    match('#')
    expression()
    print 'CMP (SP)+,D0'
    print 'SNE D0'

def less():
    match('<')
    expression()
    print 'CMP (SP)+,D0'
    print 'SGE D0'

def greater():
    match('>')
    expression()
    print 'CMP (SP)+,D0'
    print 'SLE D0'

def assignment():
    name = get_name()
    match('=')
    bool_expression()
    print('LEA ' + name + '(PC),A0')
    print('MOVE D0,(A0)')

initialize()
#bool_expression()
assignment()
if(look != stream[-1]): expected('look was ' + look + 'Newline')
