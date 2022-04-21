# [DreamHack] rev-basic-0

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 사용자에게 문자열 입력을 받아 정해진 방법으로 입력값을 검증하여 correct 또는 wrong을 출력하는 프로그램이 주어집니다.
>
> 해당 바이너리를 분석하여 correct를 출력하는 입력값을 찾으세요!
>
> 획득한 입력값은 `DH{}` 포맷에 넣어서 인증해주세요.
>
> 예시) 입력 값이 `Apple_Banana`일 경우 flag는 `DH{Apple_Banana}`
>
> Release: [rev-basic-0.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8533290/rev-basic-0.zip)

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

`input`에 문자열을 입력받는다. `check(input)`의 반환값이 0이면 Wrong, 0이 아니면 Correct를 출력한다. `check(input)`의 반환값이 0이 되지 않는 입력값을 찾으면 된다.

```c
_BOOL8 __fastcall check(const char *input)
{
  return strcmp(input, "Compar3_the_str1ng") == 0;
}
```

`strcmp()`는 두 문자열이 같은 경우 0을 반환하기 때문에, `input`이 `"Compar3_the_str1ng"`이면 `check(input)`은 1을 반환한다.

## Solve

```
PS > .\chall0.exe
Input : Compar3_the_str1ng
Correct
```

```
flag: DH{Compar3_the_str1ng}
```