# [DreamHack] rev-basic-4

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 사용자에게 문자열 입력을 받아 정해진 방법으로 입력값을 검증하여 correct 또는 wrong을 출력하는 프로그램이 주어집니다.
>
> 해당 바이너리를 분석하여 correct를 출력하는 입력값을 알아내세요.
>
> 획득한 입력값은 `DH{}` 포맷에 넣어서 인증해주세요.
>
> 예시) 입력 값이 `Apple_Banana`일 경우 flag는 `DH{Apple_Banana}`
>
> Release: [rev-basic-4.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8598164/rev-basic-4.zip)

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

`check(input)`의 반환값이 0이 아니면 Correct를 출력한다.

### check()

```c
__int64 __fastcall check(__int64 input)
{
  int i; // [rsp+0h] [rbp-18h]

  for ( i = 0; i < 0x1C; ++i )
  {
    if ( ((0x10 * *(input + i)) | (*(input + i) >> 4)) != result[i] )
      return 0i64;
  }
  return 1i64;
}
```

`0 <= i < 0x1c`인 `i`에 대해, `input[i] * 0x10 | input[i] >> 4 == result[i]`가 성립해야 한다. 즉 `input[i]`의 상위 4바이트와 하위 4바이트를 바꾼 값이 `result[i]`가 되어야 한다. 다르게 표현하면, `result[i]`의 상위 4바이트와 하위 4바이트를 바꾼 값이 `input[i]`이면 된다.

## Solve

```python
result = b"$'\x13\xc6\xc6\x13\x16\xe6G\xf5&\x96G\xf5F'\x13&&\xc6V\xf5\xc3\xc3\xf5\xe3\xe3\x00" # IDAPython> get_bytes(0x140003000, 0x1c)
flag = b''

for char in result:
    flag += bytes([(char >> 4) + ((char << 4) & 0xff)])

print(flag)
```

```
$ python3 solve.py
b'Br1ll1ant_bit_dr1bble_<<_>>\x00'
```

```
PS > .\chall4.exe
Input : Br1ll1ant_bit_dr1bble_<<_>>
Correct
```