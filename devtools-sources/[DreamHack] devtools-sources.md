# [DreamHack] devtools-sources

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 개발자 도구의 Sources 탭 기능을 활용해 플래그를 찾아보세요.
>
> Release: [devtools-sources.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8551189/devtools-sources.zip)

모든 파일로부터 `DH{`라는 문자열을 찾아보면 플래그를 얻을 수 있다. 문제 파일들이 있는 디렉토리에서 다음의 명령어를 실행한다.

```bash
grep -rn DH{ *
```

```
flag: DH{2ed07940b6fd9b0731ef698a5f0c065be9398f7fa00f03ed9da586c3ed1d54d5}
```