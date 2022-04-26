# [DreamHack] [wargame.kr] DLL with notepad

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> DLL Reverse Engineering Challenge.
> Can you reversing DLL File?

## Analysis

![image](https://user-images.githubusercontent.com/104156058/165223910-e5a1961c-09ea-496a-8690-c8618672c794.png)

서버에 접속해서 download를 누르면 문제 파일을 다운받을 수 있다. `notepad.exe`와 `blueh4g13.dll` 파일이 있는데, `notepad.exe`를 x32dbg에서 실행시켜보면 `blueh4g13.dll` 모듈이 로드되는 것을 확인할 수 있다. 문제에서도 DLL 리버싱이라고 했고, 파일 이름도 수상하고 하니 이 DLL 파일을 분석해보자.

### start()

```c
BOOL __stdcall DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
{
  if ( fdwReason == 1 )
    start(hinstDLL);
  return 1;
}
```

```c
int __cdecl start(LPVOID lpParameter)
{
  wchar_t *v1; // eax
  WCHAR Filename[256]; // [esp+4h] [ebp-204h] BYREF

  if ( GetModuleFileNameW(0, Filename, 0x200u) )
  {
    v1 = wcsrchr(Filename, 0x5Cu);
    if ( v1 )
    {
      if ( !wcsicmp(v1 + 1, L"notepad.exe") )
      {
        dword_100033A8 = (int)CreateThread(0, 0, (LPTHREAD_START_ROUTINE)StartAddress, lpParameter, 0, 0);
        CloseHandle((HANDLE)dword_100033A8);
      }
    }
  }
  return 1;
}
```

`DLLMain()`에서 `start()`를 호출하고, `start()`에서는 쓰레드를 생성하여 `StartAddress()`를 호출한다.

### StartAddress()

```c
void __stdcall __noreturn StartAddress(LPVOID lpThreadParameter)
{
  HWND WindowW; // esi
  HWND Window; // ebx
  DWORD CurrentProcessId; // edi
  DWORD dwProcessId; // [esp+14h] [ebp-28h] BYREF
  CHAR String[32]; // [esp+18h] [ebp-24h] BYREF

  sub_100010C0();
  Sleep(0x2BCu);
  WindowW = FindWindowW(0, WindowName);
  Window = FindWindowExW(WindowW, 0, L"edit", 0);
  CurrentProcessId = GetCurrentProcessId();
  GetWindowThreadProcessId(WindowW, &dwProcessId);
  if ( CurrentProcessId != dwProcessId )
    FreeLibraryAndExitThread((HMODULE)lpThreadParameter, 0);
  do
  {
    Sleep(0x32u);
    GetWindowTextA(Window, String, 32);
  }
  while ( strcmp(String, (const char *)&dword_10003388) );
  SetWindowTextA(Window, ::String);
  FreeLibraryAndExitThread((HMODULE)lpThreadParameter, 0);
}
```

`StartAddress()`에서는 `sub_100010c0()`을 호출한다.

### sub_100010c0()

`sub_100010c0()`에서는 두 개의 문자열을 인코딩하는 과정이 있다.

```c
  sub_10001320(str1, "oh! handsome guy!");
  idx = 0;
  if ( strlen(str1) )
  {
    tm_mon = Tm.tm_mon;
    v2 = Tm.tm_mday * Tm.tm_mon;
    do
    {
      v3 = v2 + str1[idx];
      v4 = 126
         * (((int)(((unsigned __int64)(0x7DF7DF7Di64 * v3) >> 32) - v3) >> 6)
          + ((unsigned int)(((unsigned __int64)(0x7DF7DF7Di64 * v3) >> 32) - v3) >> 31))
         + v3;
      if ( v4 < 0x21 )
        LOBYTE(v4) = v4 + tm_mon + 0x21;
      *((_BYTE *)&dword_10003388 + idx++) = v4;
      v2 += tm_mon;
    }
    while ( idx < strlen(str1) );
  }
```

먼저 `"oh! handsome guy!"`라는 문자열을 인코딩해서 `dword_10003388`에 저장한다.

```c
  sub_10001340(str2, "Air fares to NY don't come cheap.");
  _idx = 0;
  result = strlen(str2);
  if ( result )
  {
    tm_mday = Tm.tm_mday;
    v8 = Tm.tm_mday * Tm.tm_mon;
    do
    {
      v9 = v8 + str2[_idx];
      v10 = 126
          * (((int)(((unsigned __int64)(0x7DF7DF7Di64 * v9) >> 32) - v9) >> 6)
           + ((unsigned int)(((unsigned __int64)(0x7DF7DF7Di64 * v9) >> 32) - v9) >> 31))
          + v9;
      if ( v10 < 33 )
        LOBYTE(v10) = v10 + tm_mday + 33;
      String[_idx++] = v10;
      v8 += tm_mday;
      result = strlen(str2);
    }
    while ( _idx < result );
  }
```

다음으로 `"Air fares to NY don't come cheap."`라는 문자열을 인코딩해서 `String`에 저장한다.

정연산을 짜서 인코딩된 문자열을 구할 수도 있겠지만, 귀찮으니 그냥 디버거에서 실행시켜서 `sub_100010c0()` 함수가 리턴될 때 메모리를 보면

![image](https://user-images.githubusercontent.com/104156058/165225299-7ad18fa0-a7b9-4ccb-8899-99d091b1333f.png)

위쪽 두 줄이 `String`이고, 아래쪽이 `dword_100033a8`에 해당한다.

## Solve

`String`에 저장된 인코딩된 문자열을 서버의 auth에 넣으면 플래그를 획득할 수 있다. (왜지?)

![image](https://user-images.githubusercontent.com/104156058/165225483-0c5b7775-0690-47c9-bbee-c783932d3dfa.png)

![image](https://user-images.githubusercontent.com/104156058/165225512-11627e23-02cb-46a0-bd3d-e7cd29c3b59c.png)

```
flag: DH{969d9c5b8d4438b8e4952edce7294cb8d8407ed2}
```