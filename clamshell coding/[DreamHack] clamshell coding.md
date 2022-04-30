# [DreamHack] clamshell coding

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 드림이가 학교에서 숙제를 받았습니다.
>
> 간단한 수학 문제인데, 쉘코딩을 통해 풀어주세요!
>
> Release: [clamshell coding.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8597600/clamshell.coding.zip)

## Analysis

### server

```python
        argc = random.randint(10, 20)
        argv = [random.randint(10, 99) for _ in range(argc)]

        answer = 0
        for arg in argv:
            if arg % 3 == 0:
                answer += arg
            else:
                answer += arg * 2

        answer = answer % 100

        argv = list(map(str, argv))

        returncode = run(shellcode, argv)

        if answer != returncode:
            print("wrong!")
            print("prob:", argv)
            print("answer:", answer)
            print("your answer:", returncode)
            exit()
```

`argv`는 `argc`개의 랜덤한 두 자리 수들의 배열이다. 3의 배수는 한 번만 더하고, 3의 배수가 아닌 수는 두 번 더한다. 이 `answer`를 맞추는 `shellcode`를 짜서 입력으로 넣어야 한다.

```python
def run(shellcode, prob):
    p = subprocess.Popen(
        ["./runner", shellcode] + prob, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )

    try:
        p.wait(1)
        returncode = p.poll()
        if returncode is None:
            print("TIMEOUT!")
            exit()
    except Exception as E:
        print("something wrong!")
        print(E)
        exit()

    return returncode
```

`run()`에서는 `./runner`의 매개변수로 `shellcode`와 `prob`의 수들을 전달한다. 예를 들어 `prob`이 `[10, 11, 12, 13]`이라면 `./runner <shellcode> 10 11 12 13`을 실행하게 된다.

### runner

```c
int main(int argc, char* argv[]){
    assert(argc > 1);
    assert(strlen(argv[1]) % 2 == 0);

    size_t len = 0;
    char *shellcode = hex2bin(argv[1], &len);
    assert(strlen(argv[1]) == len * 2);

    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    seccomp_load(ctx);

    int (*foo)(int, char*[]) = (int(*)(int, char*[]))shellcode;

    return foo(argc, argv);
}
```

`runner`에서는 셸코드를 실행하고 그 셸코드의 반환값을 반환한다. Seccomp가 걸려있어서 `exit`과 `exit_group` 시스템 콜은 사용할 수 없다.

## Solve

`server.py`에서 `runner`로 전달하는 것과 같은 형식의 `argc`와 `argv`를 전달받아서 결과를 구하는 C 코드를 작성하고, 컴파일해서 그 코드를 그대로 입력하면 된다.

```c
int main(int argc, char **argv)
{
    int answer = 0;
    for (int i = 0; i < argc - 2; i++)
    {
        int number = (argv[2 + i][1] - '0') + (argv[2 + i][0] - '0') * 10;
        if (number % 3 == 0)
        {
            answer += number;
        }
        else
        {
            answer += number * 2;
        }
    }
    return answer % 100;
}
```

`argv`에 전달된 `prob`의 수들을 정수형으로 바꾸고, 그 수가 3의 배수이면 한 번만 더하고 3의 배수가 아니면 두 번 더하는 코드이다.

```python
import binascii
from pwn import *

r = remote('host1.dreamhack.games', 23211)
e = ELF('./solve')

f = open('./solve', 'rb')
shellcode = f.read()[e.symbols['main']:e.symbols['__libc_csu_init']]
f.close()
shellcode = binascii.hexlify(shellcode)

r.recvline()
r.sendline(shellcode)

r.interactive()
```

앞의 C 코드를 컴파일해서 `solve`라는 바이너리 파일을 만들고, 그 파일에서 `main()` 함수 부분만 가져와서 셸코드로 서버에 보내면 플래그를 획득할 수 있다.

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 23211: Done
[*] '/mnt/d/Github-h0meb0dy/Dreamhack-Wargame/clamshell coding/solve'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] Switching to interactive mode
DH{802bd1b3d2ee1bed3a52700c106dccd2}
```