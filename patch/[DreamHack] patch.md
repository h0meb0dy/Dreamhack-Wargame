# [DreamHack] patch

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> flag를 그리는 루틴을 분석하고 가려진 flag를 보이게 해주세요.
>
> Release: [patch.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8550745/patch.zip)

![image](https://user-images.githubusercontent.com/102066383/160338985-669b3a5d-c575-4079-8c43-f4c9e5b75824.png)

프로그램을 실행시켜보면 가려진 플래그가 나온다.

```c
  wcex.cbSize = 80;
  wcex.style = 3;
  wcex.lpfnWndProc = (WNDPROC)sub_7FF6F47832F0;
  *(_QWORD *)&wcex.cbClsExtra = 0i64;
  wcex.hInstance = hInstance;
  wcex.hIcon = LoadIconW(hInstance, (LPCWSTR)0x6B);
  CursorW = LoadCursorW(0i64, (LPCWSTR)0x7F00);
  *(__m128i *)&wcex.hbrBackground = _mm_load_si128((const __m128i *)&xmmword_7FF6F47853F0);
  wcex.hCursor = CursorW;
  wcex.lpszClassName = &ClassName;
  wcex.hIconSm = LoadIconW(hInstance, (LPCWSTR)0x6C);
  RegisterClassExW(&wcex);
```

`main()`에서 윈도우 클래스를 등록하는 코드이다. 콜백 함수를 의미하는 `lpfnWndProc`에 `sub_7FF6F47832F0()`의 주소가 들어간다.

```c
LRESULT __fastcall sub_7FF6F47832F0(HWND a1, UINT a2, WPARAM a3, LPARAM a4)
{
  _QWORD *v5; // rbx
  __int64 v6; // rbx
  __int64 v7; // [rsp+20h] [rbp-18h] BYREF

  switch ( a2 )
  {
    case 2u:
      PostQuitMessage(0);
      return 0i64;
    case 0xFu:
      qword_7FF6F4787910 = (__int64)BeginPaint(hWnd, &Paint);
      v5 = (_QWORD *)GdipAlloc(16i64);
      if ( v5 )
      {
        *v5 = 0i64;
        v5[1] = 0i64;
        v7 = 0i64;
        *((_DWORD *)v5 + 2) = GdipCreateFromHDC(qword_7FF6F4787910, &v7);
        *v5 = v7;
      }
      else
      {
        v5 = 0i64;
      }
      qword_7FF6F4787918 = (__int64)v5;
      sub_7FF6F4782C40();
      v6 = qword_7FF6F4787918;
      if ( qword_7FF6F4787918 )
      {
        GdipDeleteGraphics(*(_QWORD *)qword_7FF6F4787918);
        GdipFree(v6);
      }
      EndPaint(hWnd, &Paint);
      return 0i64;
    case 0x202u:
      InvalidateRect(hWnd, 0i64, 1);
      UpdateWindow(hWnd);
      return 0i64;
    default:
      return DefWindowProcW(a1, a2, a3, a4);
  }
}
```

`case 0xF`의 경우에 `BeginPaint()`와 `EndPaint()`가 호출되는 것을 보아 그림이 그려지는 부분이라고 추측할 수 있다. 이 부분에 있는 `sub_7FF6F4782C40()` 함수를 보면,

```c
  sub_7FF6F4782B80((unsigned int)qword_7FF6F4787880, a2, 30u, 470, 80, 0xFF000000);
  sub_7FF6F4782B80(v2, v3, 35u, 470, 75, 0xFF000000);
  sub_7FF6F4782B80(v2, v4, 40u, 470, 70, 0xFF000000);
  sub_7FF6F4782B80(v2, v5, 45u, 470, 65, 0xFF000000);
  sub_7FF6F4782B80(v2, v6, 50u, 470, 60, 0xFF000000);
  sub_7FF6F4782B80(v2, v7, 55u, 470, 55, 0xFF000000);
  sub_7FF6F4782B80(v2, v8, 60u, 470, 50, 0xFF000000);
  sub_7FF6F4782B80(v2, v9, 65u, 470, 45, 0xFF000000);
  sub_7FF6F4782B80(v2, v10, 70u, 470, 40, 0xFF000000);
  sub_7FF6F4782B80(v2, v11, 75u, 470, 75, 0xFF000000);
  sub_7FF6F4782B80(v2, v12, 80u, 400, 60, 0xFF000000);
  sub_7FF6F4782B80(v2, v13, 30u, 470, 90, 0xFF000000);
  sub_7FF6F4782B80(v2, v14, 35u, 470, 30, 0xFF000000);
  sub_7FF6F4782B80(v2, v15, 40u, 470, 35, 0xFF000000);
  sub_7FF6F4782B80(v2, v16, 45u, 470, 50, 0xFF000000);
  sub_7FF6F4782B80(v2, v17, 50u, 470, 40, 0xFF000000);
  sub_7FF6F4782B80(v2, v18, 55u, 400, 90, 0xFF000000);
  sub_7FF6F4782B80(v2, v19, 60u, 470, 60, 0xFF000000);
  sub_7FF6F4782B80(v2, v20, 65u, 470, 30, 0xFF000000);
  sub_7FF6F4782B80(v2, v21, 70u, 470, 80, 0xFF000000);
  sub_7FF6F4782B80(v2, v22, 75u, 470, 70, 0xFF000000);
  sub_7FF6F4782B80(v2, v23, 80u, 470, 60, 0xFF000000);
  sub_7FF6F4782B80(v2, v24, 80u, 470, 80, 0xFF000000);
  sub_7FF6F4782B80(v2, v25, 80u, 470, 70, 0xFF000000);
  sub_7FF6F4782B80(v2, v26, 90u, 470, 90, 0xFF000000);
  v27 = qword_7FF6F4787880;
  sub_7FF6F47817A0(qword_7FF6F4787880, 40i64, v28, 0xFF000000);
  sub_7FF6F4781C80(v27, 80i64, v29, 0xFF000000);
  sub_7FF6F4782640(v27, v30, v31, 0xFF000000i64);
  sub_7FF6F47820F0(v27, v32, v33, 0xFF000000i64);
  sub_7FF6F4782390(v27, v34, v35, 0xFF000000i64);
  sub_7FF6F4781240(v27, v36, v37, 0xFF000000i64);
  sub_7FF6F4781F20(v27, v38, v39, 0xFF000000i64);
  sub_7FF6F4781560(v27, v40, v41, 0xFF000000i64);
  sub_7FF6F4781C80(v27, 360i64, v42, 0xFF000000);
  sub_7FF6F47819D0(v27, v43, v44, 0xFF000000i64);
  sub_7FF6F47817A0(v27, 440i64, v45, 0xFF000000);
  sub_7FF6F4782870(v27, v46, v47, 0xFF000000i64);
  return 0;
```

`sub_7FF6F4782B80()`와, 그와 비슷한 형태의 함수들이 반복적으로 호출된다.

```c
__int64 __fastcall sub_7FF6F4782B80(__int64 a1, __int64 a2, unsigned int a3, int a4, int a5, unsigned int a6)
{
  int v9; // eax
  __int64 v10; // rsi
  int v11; // eax
  __int64 v12; // rbx
  int v13; // eax
  __int64 v15; // [rsp+30h] [rbp-38h] BYREF
  __int64 v16; // [rsp+38h] [rbp-30h]

  v16 = 0i64;
  v15 = 0i64;
  v9 = GdipCreatePen1(a6, a2, 0i64, &v15);
  v10 = *(_QWORD *)(a1 + 120);
  LODWORD(v16) = v9;
  v11 = GdipDrawLineI(*(_QWORD *)v10, v15, 150i64, a3, a4, a5);
  if ( v11 )
    *(_DWORD *)(v10 + 8) = v11;
  v12 = *(_QWORD *)(a1 + 120);
  v13 = GdipSetSmoothingMode(*(_QWORD *)v12, 4i64);
  if ( v13 )
    *(_DWORD *)(v12 + 8) = v13;
  return GdipDeletePen(v15);
}
```

`sub_7FF6F4782B80()`을 보면 `GdipCreatePen1()`로 펜을 생성하고, `GdipDrawLineI()`로 선을 하나 그린다. 이 함수가 처음 호출될 때 bp를 걸고 전후 상태를 비교해보면 다음과 같다.

![image](https://user-images.githubusercontent.com/102066383/160343088-8006a4c1-b3ef-43f2-bcd8-f71280dedfcd.png)

![image](https://user-images.githubusercontent.com/102066383/160343146-58f0f88c-b13e-4be1-b0b4-01cb9565fd9e.png)

이 결과로부터, `sub_7FF6F4782B80()`는 플래그를 가리는 선을 그리는 함수라고 추측할 수 있다. 이 함수의 첫 번째 바이트를 `c3`(`ret`)으로 패치해서 아무 동작도 하지 않도록 만들고 실행하면 다음의 결과를 얻는다.

![image](https://user-images.githubusercontent.com/102066383/160345115-87198e24-c599-482c-b23f-d7ab5ca36d92.png)

```
flag: DH{UPATCHED}
```
