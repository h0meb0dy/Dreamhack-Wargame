# [DreamHack] rev-basic-3

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 사용자에게 문자열 입력을 받아 정해진 방법으로 입력값을 검증하여 correct 또는 wrong을 출력하는 프로그램이 주어집니다.
>
> 해당 바이너리를 분석하여 correct를 출력하는 입력값을 찾으세요!
>
> 획득한 입력값은 `DH{}` 포맷에 넣어서 인증해주세요.
>
> 예시) 입력 값이 `Apple_Banana`일 경우 flag는 `DH{Apple_Banana}`
>
> Release: [rev-basic-3.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8551088/rev-basic-3.zip)

## Analysis

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

`input`에 문자열을 입력받고, `check(input)`의 반환값이 0이 아니면 Correct를 출력한다.

```c
__int64 __fastcall check(__int64 input)
{
  int i; // [rsp+0h] [rbp-18h]

  for ( i = 0; (unsigned __int64)i < 0x18; ++i )
  {
    if ( result[i] != (i ^ *(unsigned __int8 *)(input + i)) + 2 * i )
      return 0i64;
  }
  return 1i64;
}
```

`check()`에서는 `input[0]`부터 `input[17]`까지, `result[i] == i ^ input[i] + 2 * i`를 만족하면 1을 반환한다. 역연산을 수행하여 이 조건을 만족시키기 위해 필요한 `input[i]`를 구할 수 있다.

## Solve

```python
result = b'I`gtcgBf\x80xii{\x99m\x88h\x94\x9f\x8dM\xa5\x9dE\x00\x00\x00\x00\x00\x00\x00\x00' # IDAPython> get_bytes(0x140003000, 0x20)
flag = b''

for i in range(0x18):
    flag += bytes([(result[i] - 2 * i) ^ i])

print(flag)
```

```
PS > python .\solve.py
b'I_am_X0_xo_Xor_eXcit1ng\x00'
```

```
flag: DH{I_am_X0_xo_Xor_eXcit1ng}
```