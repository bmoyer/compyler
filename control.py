#!/usr/local/bin/python

stream = raw_input()
idx = 0
# label counter
lcount = 0 
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
    global stream
    if len(stream) == 0:
        exit(0)
    look = stream[0]
    stream = stream[1::1]

def initialize():
    lcount = 0
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

def get_name():
    if look.isalpha():
        old_look = look
        get_char()
        return old_look.upper()
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

def new_label():
    global lcount
    s = str(lcount)
    label = 'L' + s
    lcount += 1
    return label

def post_label(l):
    print l + ':'

def do_program():
    block()
    if look != 'e':
        expected('end')
    print('END')

def do_if():
    match('i')
    condition()
    l1= new_label()
    l2 = l1
    print 'BEQ ' + l1
    block()
    if look == 'l':
        match('l')
        l2 = new_label()
        print 'BRA ' + l2
        post_label(l1)
        block()
    match('e')
    post_label(l2)

def block():
    while not (look in ['e', 'l']):
        #print "look was ", look
        old_look = look
        if old_look == 'i':
            do_if()
            continue
        else: 
            other()
            continue

def condition():
    print('<condition>')

def other():
    print get_name()

def assignment():
    name = get_name()
    match('=')
    expression()
    print('LEA ' + name + '(PC),A0')
    print('MOVE D0,(A0)')

initialize()
do_program()
#if(look != stream[-1]): expected('Newline')
