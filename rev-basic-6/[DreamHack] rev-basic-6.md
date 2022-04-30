# [DreamHack] rev-basic-6

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 사용자에게 문자열 입력을 받아 정해진 방법으로 입력값을 검증하여 correct 또는 wrong을 출력하는 프로그램이 주어집니다.
>
> 해당 바이너리를 분석하여 correct를 출력하는 입력값을 찾으세요!
>
> 획득한 입력값은 `DH{}` 포맷에 넣어서 인증해주세요.
>
> 예시) 입력 값이 `Apple_Banana`일 경우 flag는 `DH{Apple_Banana}`
>
> Release: [rev-basic-6.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8596104/rev-basic-6.zip)

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
    if ( chars[*(unsigned __int8 *)(input + i)] != result[i] )
      return 0i64;
  }
  return 1i64;
}
```

`0 <= i < 0x12`인 `i`에 대해, `chars[input[i]] == result[i]`가 성립해야 한다.

## Solve

```python
result = b'\x00MQP\xef\xfb\xc3\xcf\x92EM\xcf\xf5\x04@PCc' # IDAPython> get_bytes(0x140003000, 0x12)
chars = b'c|w{\xf2ko\xc50\x01g+\xfe\xd7\xabv\xca\x82\xc9}\xfaYG\xf0\xad\xd4\xa2\xaf\x9c\xa4r\xc0\xb7\xfd\x93&6?\xf7\xcc4\xa5\xe5\xf1q\xd81\x15\x04\xc7#\xc3\x18\x96\x05\x9a\x07\x12\x80\xe2\xeb\'\xb2u\t\x83,\x1a\x1bnZ\xa0R;\xd6\xb3)\xe3/\x84S\xd1\x00\xed \xfc\xb1[j\xcb\xbe9JLX\xcf\xd0\xef\xaa\xfbCM3\x85E\xf9\x02\x7fP<\x9f\xa8Q\xa3@\x8f\x92\x9d8\xf5\xbc\xb6\xda!\x10\xff\xf3\xd2\xcd\x0c\x13\xec_\x97D\x17\xc4\xa7~=d]\x19s`\x81O\xdc"*\x90\x88F\xee\xb8\x14\xde^\x0b\xdb\xe02:\nI\x06$\\\xc2\xd3\xacb\x91\x95\xe4y\xe7\xc87m\x8d\xd5N\xa9lV\xf4\xeaez\xae\x08\xbax%.\x1c\xa6\xb4\xc6\xe8\xddt\x1fK\xbd\x8b\x8ap>\xb5fH\x03\xf6\x0ea5W\xb9\x86\xc1\x1d\x9e\xe1\xf8\x98\x11i\xd9\x8e\x94\x9b\x1e\x87\xe9\xceU(\xdf\x8c\xa1\x89\r\xbf\xe6BhA\x99-\x0f\xb0T\xbb\x16' # IDAPython> get_bytes(0x140003020, 0x100)

flag = ''

for idx in range(len(result)):
    flag += chr(chars.index(result[idx]))

print('DH{' + flag + '}')
```

```
$ python3 solve.py
DH{Replac3_the_w0rld}
```