# [DreamHack] [wargame.kr] plz variable

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Can you find the solution quickly in polynomials?

## Analysis

```
$ nc host1.dreamhack.games 18573
Please match the correct answer 30 times.
Submit format -> a,b,c,d,,,(Ascending order)
Timeout = 60sec
a,b,c,d,,, is natural number
a,b,c,d,,, is 100 <=  <= 1000

1th...
b + f + d + c + h + g + a + e = 5401
c * e + g - a * h - b - d * f = -136215
h + d - g + b * a + e + c * f = 1014061
e - g - f - h - a + d + c - b = -1739
f * d + a + b - h + g * e - c = 1101536
a - b + e - f + h - g - d - c = -1141
f - c + h + b + g + e - d - a = 1833
b + h + e * f - g - a - c - d = 430895
Answer ->
```

n개의 변수와 n개의 식이 주어지고, 60초 안에 30번 정답을 맞추면 플래그를 준다. `z3`를 이용해서 해결할 수 있다.

## Solve

```python
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
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 18573: Done
[*] attempt 1
[*] attempt 2
[*] attempt 3
[*] attempt 4
[*] attempt 5
[*] attempt 6
[*] attempt 7
[*] attempt 8
[*] attempt 9
[*] attempt 10
[*] attempt 11
[*] attempt 12
[*] attempt 13
[*] attempt 14
[*] attempt 15
[*] attempt 16
[*] attempt 17
[*] attempt 18
[*] attempt 19
[*] attempt 20
[*] attempt 21
[*] attempt 22
[*] attempt 23
[*] attempt 24
[*] attempt 25
[*] attempt 26
[*] attempt 27
[*] attempt 28
[*] attempt 29
[*] attempt 30
[*] Switching to interactive mode


Flag is DH{359125f28efb45825d56ff1738cd35aee8f8029b}
```