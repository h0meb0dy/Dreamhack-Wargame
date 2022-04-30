# [DreamHack] rev-basic-2

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 사용자에게 문자열 입력을 받아 정해진 방법으로 입력값을 검증하여 correct 또는 wrong을 출력하는 프로그램이 주어집니다.
>
> 해당 바이너리를 분석하여 correct를 출력하는 입력값을 찾으세요!
>
> 획득한 입력값은 `DH{}` 포맷에 넣어서 인증해주세요.
>
> 예시) 입력 값이 `Apple_Banana`일 경우 flag는 `DH{Apple_Banana}`
>
> Release: [rev-basic-2.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8580601/rev-basic-2.zip)

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

  for ( i = 0; (unsigned __int64)i < 0x12; ++i )
  {
    if ( *(_DWORD *)&result[4 * i] != *(unsigned __int8 *)(input + i) )
      return 0i64;
  }
  return 1i64;
}
```

`i < 0x12`인 `i`에 대해 `input[i] == result[i]`이면 1을 반환한다.

## Solve

![image](https://user-images.githubusercontent.com/104156058/165706708-27b6ae8f-872b-4076-805e-229628d7eb5c.png)

`result`에 있는 값들을 모두 이어붙이면 플래그가 된다.

```
PS > .\chall2.exe
Input : Comp4re_the_arr4y
Correct
```

```
flag: DH{Comp4re_the_arr4y}
```