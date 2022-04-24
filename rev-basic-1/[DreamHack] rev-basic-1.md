# [DreamHack] rev-basic-1

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 사용자에게 문자열 입력을 받아 정해진 방법으로 입력값을 검증하여 correct 또는 wrong을 출력하는 프로그램이 주어집니다.
>
> 해당 바이너리를 분석하여 correct를 출력하는 입력값을 알아내세요.
>
> 획득한 입력값은 `DH{}` 포맷에 넣어서 인증해주세요.
>
> 예시) 입력 값이 `Apple_Banana`일 경우 flag는 `DH{Apple_Banana}`
>
> Release: [rev-basic-1.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8550686/rev-basic-1.zip)

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

`input`에 문자열을 입력받는다. `check(input)`의 반환값이 0이면 Wrong을 출력하고, 0이 아니면 Correct를 출력한다.

```c
_BOOL8 __fastcall check(_BYTE *input)
{
  if ( *input != 'C' )
    return 0i64;
  if ( input[1] != 'o' )
    return 0i64;
  if ( input[2] != 'm' )
    return 0i64;
  if ( input[3] != 'p' )
    return 0i64;
  if ( input[4] != 'a' )
    return 0i64;
  if ( input[5] != 'r' )
    return 0i64;
  if ( input[6] != '3' )
    return 0i64;
  if ( input[7] != '_' )
    return 0i64;
  if ( input[8] != 't' )
    return 0i64;
  if ( input[9] != 'h' )
    return 0i64;
  if ( input[10] != 'e' )
    return 0i64;
  if ( input[11] != '_' )
    return 0i64;
  if ( input[12] != 'c' )
    return 0i64;
  if ( input[13] != 'h' )
    return 0i64;
  if ( input[14] != '4' )
    return 0i64;
  if ( input[15] != 'r' )
    return 0i64;
  if ( input[16] != 'a' )
    return 0i64;
  if ( input[17] != 'c' )
    return 0i64;
  if ( input[18] != 't' )
    return 0i64;
  if ( input[19] != '3' )
    return 0i64;
  if ( input[20] == 'r' )
    return input[21] == 0;
  return 0i64;
}
```

`check()`는 `input`의 각 문자가 조건을 만족하는지 검사한다. 모든 조건을 만족하면 1을 반환한다. 이 문자들을 모두 이으면 플래그가 된다.

## Solve

```
PS > .\chall1.exe
Input : Compar3_the_ch4ract3r
Correct
```

```
flag: DH{Compar3_the_ch4ract3r}
```