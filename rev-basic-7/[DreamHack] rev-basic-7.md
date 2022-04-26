# [DreamHack] rev-basic-7

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 사용자에게 문자열 입력을 받아 정해진 방법으로 입력값을 검증하여 correct 또는 wrong을 출력하는 프로그램이 주어집니다.
>
> 해당 바이너리를 분석하여 correct를 출력하는 입력값을 알아내세요.
>
> 획득한 입력값은 `DH{}` 포맷에 넣어서 인증해주세요.
>
> 예시) 입력 값이 `Apple_Banana`일 경우 flag는 `DH{Apple_Banana}`
>
> Release: [rev-basic-7.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8560031/rev-basic-7.zip)

## Analysis

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char input[256]; // [rsp+20h] [rbp-118h] BYREF

  memset(input, 0, sizeof(input));
  printf("Input : ", argv, envp);
  scanf("%256s", input);
  if ( (unsigned int)check(input) )
    puts("Correct");
  else
    puts("Wrong");
  return 0;
}
```

`check(input)`의 반환값이 0이 아니면 Correct를 출력한다.

```c
__int64 __fastcall check(__int64 input)
{
  int i; // [rsp+0h] [rbp-18h]

  for ( i = 0; (unsigned __int64)i < 0x1F; ++i )
  {
    if ( (i ^ (unsigned __int8)__ROL1__(*(_BYTE *)(input + i), i & 7)) != result[i] )
      return 0i64;
  }
  return 1i64;
}
```

`input[i]`를 `i & 7`만큼 rotate left 연산하고, 그 결과값을 `i`와 xor 연산한 결과가 `result[i]`와 같아야 한다. 역연산(`input[i] = ROR(result[i] ^ i, i & 7)`)을 구현해서 올바른 `input`을 구할 수 있다.

## Solve

```python
# rotate right
def ror(value, n):
    return (value >> n) + ((value << (8 - n)) & 0xff)

result = b'R\xdf\xb3`\xf1\x8b\x1c\xb5W\xd1\x9f8K)\xd9&\x7f\xc9\xa3\xe9S\x18O\xb8j\xcb\x87X[9\x1e\x00' # IDAPython> get_bytes(0x140003000, 0x20)
input_bytes = b''

for idx in range(0x1f):
    input_bytes += bytes([ror(result[idx] ^ idx, idx & 7)])

print(input_bytes)
```

```
$ python3 solve.py
b'Roll_the_left!_Roll_the_right!\x00'
```

```
PS > .\chall7.exe
Input : Roll_the_left!_Roll_the_right!
Correct
```

```
flag: DH{Roll_the_left!_Roll_the_right!}
```