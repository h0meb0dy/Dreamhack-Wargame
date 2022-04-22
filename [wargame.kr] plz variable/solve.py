from pwn import *
from z3 import *

r = remote('host1.dreamhack.games', 18573)

for attempt in range(30):
    log.info('attempt ' + str(attempt + 1))

    # receive problem
    r.recvuntil(b'th...\n')
    equations = r.recvuntil(b'Answer -> ').split(b'\n')
    equations.pop()

    # declare z3 solver
    s = Solver()

    # declare variables
    for n in range(len(equations)):
        var = chr(ord('a') + n)
        exec(var + ' = Int(\'' + var + '\')')
        s.add(eval(var + '>= 100'))
        s.add(eval(var + '<= 1000'))

    # solve problem
    for equation in equations:
        s.add(eval(equation.replace(b'=', b'==')))
    s.check()
    answer = s.model()

    # submit answer
    submit = b''
    for i in range(len(answer)):
        submit += str(answer[eval(chr(ord('a') + i))]).encode()
        if i != len(answer) - 1:
            submit += b','
    r.sendline(submit)

r.interactive()