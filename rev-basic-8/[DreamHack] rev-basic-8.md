# [DreamHack] rev-basic-8

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 사용자에게 문자열 입력을 받아 정해진 방법으로 입력값을 검증하여 correct 또는 wrong을 출력하는 프로그램이 주어집니다.
>
> 해당 바이너리를 분석하여 correct를 출력하는 입력값을 찾으세요!
>
> 획득한 입력값은 `DH{}` 포맷에 넣어서 인증해주세요.
>
> 예시) 입력 값이 `Apple_Banana`일 경우 flag는 `DH{Apple_Banana}`
>
> Release: [rev-basic-8.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8557488/rev-basic-8.zip)

## Analysis

### main()

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char input[256]; // [rsp+20h] [rbp-118h] BYREF

  memset(input, 0, sizeof(input));
  printf("Input : ");
  scanf("%256s", input);
  if ( (unsigned int)check(input) )
    puts("Correct");
  else
    puts("Wrong");
  return 0;
}
```

`input`에 입력을 받고, `check(input)`의 리턴값이 0이 아니면 Correct를 출력한다.

### check()

```python
__int64 __fastcall check(__int64 input)
{
  int i; // [rsp+0h] [rbp-18h]

  for ( i = 0; (unsigned __int64)i < 0x15; ++i )
  {
    if ( (unsigned __int8)(-5 * *(_BYTE *)(input + i)) != result[i] )
      return 0i64;
  }
  return 1i64;
}
```

`input`의 각 문자에 대해, `-5 * input[i] == result[i]`가 성립해야 한다.

## Solve

조건을 만족하는 `input[i]`는 0부터 `0x100` 사이에 있으므로, 브루트포싱을 통해 답을 구할 수 있다.

```python
result = b'\xac\xf3\x0c%\xa3\x10\xb7%\x16\xc6\xb7\xbc\x07%\x02\xd5\xc6\x11\x07\xc5\x00' # IDAPython> get_bytes(0x140003000, 0x15)
flag = b''

for idx in range(0x15):
    for i in range(0x100):
        if (-5 * i) % 0x100 == result[idx]:
            flag += bytes([i])

print(flag)
```

```
$ python3 solve.py
b'Did_y0u_brute_force?\x00'
```

```
flag: DH{Did_y0u_brute_force?}
```