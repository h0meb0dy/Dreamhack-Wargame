# [DreamHack] Inject ME!!!

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 드림이가 수상한 DLL 파일을 획득하였습니다.
>
> DLL 파일과 함께 있던 TXT 파일에는 조건을 맞춰서 DLL을 로드시키면 플래그를 얻을 수 있다고만 쓰여 있었습니다.
>
> 어떻게 해야 DLL 파일을 로드할 수 있을까요?
>
> Release: [Inject ME!!!.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8560217/Inject.ME.zip)

## Analysis

![image](https://user-images.githubusercontent.com/104156058/165231504-333f7b3b-8aa0-4d07-9d62-3ede83a89c72.png)

`dreamhack.exe`라는 수상한 문자열이 있다. 이 문자열은 `sub_1800011a0()` 함수에서 참조한다.

```c
  GetModuleFileNameA(0i64, Filename, 0x104u);
  Str1 = PathFindFileNameA(Filename);
  if ( !strncmp(Str1, "dreamhack.exe", 13ui64) )
  {
    memset(v19, 0, sizeof(v19));
    for ( i = 0i64; i < 0x10; ++i )
    {
      GetModuleFileNameA(0i64, pszPath, 0x104u);
      FileNameA = PathFindFileNameA(pszPath);
      v7 = FileNameA;
      v8 = FileNameA;
      v19[i] = __ROL4__(*(_DWORD *)FileNameA, i);
    }
    sub_180001010(v19);
    for ( j = 0i64; j < 0x64; ++j )
      sub_180001060();
    *(_DWORD *)Text = 0x69D39C88;
    v10 = 0x373BD62B;
    v11 = 0x77DA5F29;
    v12 = 0x3BEA33A2;
    v13 = 0xC46D7B5E;
    v14 = 0x74C02E0E;
    v15 = 0xB153FD7E;
    v16 = 0x6FA8018A;
    v17 = 0x58504179;
    v18 = 0xD7F8990A;
    for ( k = 0i64; k < 0xA; ++k )
      *(_DWORD *)&Text[4 * k] ^= sub_180001060();
    MessageBoxA(0i64, Text, "flag", 0);
  }
  return sub_1800013E0((unsigned __int64)&v1 ^ v22);
```

`sub_1800011a0()` 함수에서는, `GetModuleFileNameA()` 함수로 실행 중인 프로세스의 경로명을 `Filename`으로 가져오고, 다시 `PathFindFileNameA(Filename)`으로 실행한 파일의 이름을 `Str1`에 저장한다. 그리고 이 문자열이 `"dreamhack.exe"`이면 조건문 안쪽으로 들어간다.

조건문 안쪽에서는 `Text`부터 `v18`까지 저장된 값들을 4바이트씩 `sub_180001060()`의 반환값과 xor 연산하고, 그 결과로 `Text`에 저장된 문자열을 `MessageBoxA()`로 출력한다. 메시지 창의 이름이 flag인 것으로 보아 플래그를 출력해줄 것 같다.

결론은, `dreamhack.exe`라는 이름의 프로그램을 실행했을 때 내부에서 이 DLL 파일을 `LoadLibrary()` 함수를 통해 로드하면, `DllEntryPoint()->sub_1800015F0()->sub_180001390()->sub_1800011A0()`의 과정을 거쳐 플래그를 출력하게 된다.

## Solve

```c
#include <windows.h>

int main() {
    LoadLibrary("prob_rev.dll");
    return 0;
}
```

위의 코드를 컴파일하고 실행하면

![image](https://user-images.githubusercontent.com/104156058/165233173-631e15a7-9947-419d-979b-4e91a3b7ec96.png)

플래그를 획득할 수 있다.

```
flag: DH{e7024e9341eb676b116edb69f37e86bf}
```