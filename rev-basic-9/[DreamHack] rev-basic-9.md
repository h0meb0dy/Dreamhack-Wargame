# [DreamHack] rev-basic-9

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 사용자에게 문자열 입력을 받아 정해진 방법으로 입력값을 검증하여 correct 또는 wrong을 출력하는 프로그램이 주어집니다.
>
> 해당 바이너리를 분석하여 correct를 출력하는 입력값을 찾으세요!
>
> 획득한 입력값은 `DH{}` 포맷에 넣어서 인증해주세요.
>
> 예시) 입력 값이 `Apple_Banana`일 경우 flag는 `DH{Apple_Banana}`
>
> Release: [rev-basic-9.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8595353/rev-basic-9.zip)

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
_BOOL8 __fastcall check(const char *input)
{
  int i; // [rsp+20h] [rbp-18h]
  int input_len; // [rsp+24h] [rbp-14h]

  input_len = strlen(input);
  if ( (input_len + 1) % 8 )                    // input length must be (8n - 1)
    return 0i64;
  for ( i = 0; i < input_len + 1; i += 8 )
    encode((unsigned __int8 *)&input[i]);
  return memcmp(input, &correct_result, 0x19ui64) == 0;
}
```

`input`의 길이에 1을 더했을 때 8로 나누어떨어져야 한다.

`input`을 8바이트씩 나눠서 `encode()` 함수에 넣고 인코딩한다. 그 결과가 `correct_result`에 저장된 값과 같으면 1을 반환한다.

### encode()

```c
__int64 __fastcall encode(unsigned __int8 *input)
{
  __int64 result; // rax
  unsigned __int8 value; // [rsp+0h] [rbp-48h]
  int j; // [rsp+4h] [rbp-44h]
  int i; // [rsp+8h] [rbp-40h]
  char key[16]; // [rsp+10h] [rbp-38h] BYREF

  strcpy(key, "I_am_KEY");
  result = *input;
  value = *input;
  for ( i = 0; i < 16; ++i )
  {
    for ( j = 0; j < 8; ++j )
    {
      value = __ROR1__(input[((_BYTE)j + 1) & 7] + chars[(unsigned __int8)key[j] ^ value], 5);
      input[((_BYTE)j + 1) & 7] = value;
    }
    result = (unsigned int)(i + 1);
  }
  return result;
}
```

`key`에는 `"I_am_KEY"`라는 문자열이 저장된다.

`0 <= j < 8`인 `j`에 대해, `input[(j + 1) & 7]`에는 원래 있던 값을 `key[j] ^ value`를 더하고 5비트만큼 rotate right한 결과값이 들어간다. `value`의 초기값은 `input[0]`이다. 이 과정을 16번 반복한다.

## Solve

`input[(j + 1) & 7]`의 새로운 값을 계산하기 위해 기존의 값과 `input[j & 7]`의 (새로운) 값을 사용한다. 따라서 역연산을 구현하여 `input[(j + 1) & 7]`의 새로운 값으로부터 기존의 값을 알아낼 수 있다. `j`를 7부터 0까지 감소시키면서 기존의 값을 구하는 과정을 16번 반복하면 올바른 `input`의 한 부분(8바이트)을 알아낼 수 있다.

```python
# rotate left
def rol(char, n):
    return ((char << n) & 0xff) + (char >> (8 - n))

key = b'I_am_KEY'
correct_result = b'~}\x9a\x8b%-\xd5=\x03+8\x98\'\x9fO\xbc*y\x00}\xc4*OX' # IDAPython> get_bytes(0x140004000, 0x18)
chars = b'c|w{\xf2ko\xc50\x01g+\xfe\xd7\xabv\xca\x82\xc9}\xfaYG\xf0\xad\xd4\xa2\xaf\x9c\xa4r\xc0\xb7\xfd\x93&6?\xf7\xcc4\xa5\xe5\xf1q\xd81\x15\x04\xc7#\xc3\x18\x96\x05\x9a\x07\x12\x80\xe2\xeb\'\xb2u\t\x83,\x1a\x1bnZ\xa0R;\xd6\xb3)\xe3/\x84S\xd1\x00\xed \xfc\xb1[j\xcb\xbe9JLX\xcf\xd0\xef\xaa\xfbCM3\x85E\xf9\x02\x7fP<\x9f\xa8Q\xa3@\x8f\x92\x9d8\xf5\xbc\xb6\xda!\x10\xff\xf3\xd2\xcd\x0c\x13\xec_\x97D\x17\xc4\xa7~=d]\x19s`\x81O\xdc"*\x90\x88F\xee\xb8\x14\xde^\x0b\xdb\xe02:\nI\x06$\\\xc2\xd3\xacb\x91\x95\xe4y\xe7\xc87m\x8d\xd5N\xa9lV\xf4\xeaez\xae\x08\xbax%.\x1c\xa6\xb4\xc6\xe8\xddt\x1fK\xbd\x8b\x8ap>\xb5fH\x03\xf6\x0ea5W\xb9\x86\xc1\x1d\x9e\xe1\xf8\x98\x11i\xd9\x8e\x94\x9b\x1e\x87\xe9\xceU(\xdf\x8c\xa1\x89\r\xbf\xe6BhA\x99-\x0f\xb0T\xbb\x16' # IDAPython> get_bytes(0x140004020, 0x100)

input_arr = [correct_result[idx] for idx in range(len(correct_result))]

# inverse operation
for idx in reversed(range(3)):
    for i in range(16):
        for j in reversed(range(8)):
            input_arr[idx * 8 + ((j + 1) & 7)] = (rol(input_arr[idx * 8 + ((j + 1) & 7)], 5) - chars[key[j] ^ input_arr[idx * 8 + (j & 7)]]) & 0xff

# get flag
flag = ''
for idx in range(len(input_arr)):
    flag += chr(input_arr[idx])
print('DH{' + flag + '}')
```

```
$ python3 solve.py
DH{Reverse__your__brain_;)}
```
