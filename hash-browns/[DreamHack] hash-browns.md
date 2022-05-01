# [DreamHack] hash-browns

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 올바르게 입력했을 때 출력되는 Flag를 구해주세요.
>
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [hash-browns.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8597948/hash-browns.zip)

## Analysis

```c
  memset(input, 0, 256);
  printf("Input : ");
  fflush(stdout);
  read(0, input, 0x100uLL);
  v5 = strchr((const char *)input, 10);
  if ( v5 )
    *v5 = 0;
  for ( i = 0; i <= 8; ++i )
  {
    ((void (__fastcall *)(char *))((char *)&unk_1208 + 1))(v6);
    sub_125C(v6, (char *)input + (int)(3 * i), 3LL);
    sub_13E7(v6);
    if ( memcmp(&v7, &result[2 * (int)i], 0x10uLL) )
    {
      puts("Wrong!");
      return 1LL;
    }
  }
  *((_BYTE *)input + (int)(3 * i)) = 0;
  printf("Correct! Flag is %s\n", (const char *)input);
  return 0LL;
```

`input`에 문자열을 입력하고, 어떤 과정을 거쳐 인코딩한 결과가 `v7`에 저장되는데, 이 값이 `result`에 있는 값과 같아지는 입력 값이 플래그가 된다. 반복문을 돌며 `sub_125c()`에 `input + 3 * i`와 3을 인자로 전달하는 것으로 보아, `input`에서 3바이트씩 나누어 처리한다는 것과, 3바이트를 인코딩한 결과는 `result[2 * i]`의 `0x10`바이트가 되어야 한다는 것을 추측할 수 있다.

```c
  result[0] = 0xFE5D3A093968D02BLL;
  result[1] = 0xBA0AA367C2862EAELL;
  result[2] = 0x8BEA2ADA9E26604FLL;
  result[3] = 0x2E6F41C96DCF5224LL;
  result[4] = 0x7FD91BD2949B75F3LL;
  result[5] = 0x5B1ED8E6072F3A6LL;
  result[6] = 0xC94045C6D4887611LL;
  result[7] = 0x9D43DF6DF6B94D95LL;
  result[8] = 0xB9A8A83C8AC08D80LL;
  result[9] = 0x6D78E80376518464LL;
  result[10] = 0xE81A20F2023C2D0LL;
  result[11] = 0x2E41EAE69D89F186LL;
  result[12] = 0x425C831DD2A3E5FDLL;
  result[13] = 0x82788DBBDC4100ECLL;
  result[14] = 0x6D0FEE8D3901DD20LL;
  result[15] = 0xEBE82A0A41E5D783LL;
  result[16] = 0x2AFA26414B72E506LL;
  result[17] = 0xD1848E9C21D114DLL;
```

플래그의 맨 앞 3글자가 `DH{`인 것을 알고 있으니, `DH{`를 입력해보면

![image](https://user-images.githubusercontent.com/104156058/166128864-d09c97b6-8695-4918-947f-c69c06a7327f.png)

`result`와 일치하는 결과가 나오는 것을 확인할 수 있다. 따라서 `DH{`를 인코딩한 결과를 hex 문자열로 표현하면, `result[0]`과 `result[1]`를 이어붙인 `2bd06839093a5dfeae2e86c267a30aba`가 된다.

> https://www.pelock.com/products/hash-calculator

그리고 이 값은

![image](https://user-images.githubusercontent.com/104156058/166128894-665a1aa0-c65b-489e-89c8-8e4c7199f406.png)

`DH{`에 MD5 해시를 씌운 값이다.

결론적으로, 플래그를 3글자씩 나누어 MD5 해시 연산을 했을 때, `result`에 있는 값이 나와야 한다. 3글자씩 브루트포싱을 하면 플래그를 획득할 수 있다.

## Solve

```python
import string
from pwn import *
import hashlib

result = [0 for i in range(18)]
result[0] = 0xFE5D3A093968D02B
result[1] = 0xBA0AA367C2862EAE
result[2] = 0x8BEA2ADA9E26604F
result[3] = 0x2E6F41C96DCF5224
result[4] = 0x7FD91BD2949B75F3
result[5] = 0x5B1ED8E6072F3A6
result[6] = 0xC94045C6D4887611
result[7] = 0x9D43DF6DF6B94D95
result[8] = 0xB9A8A83C8AC08D80
result[9] = 0x6D78E80376518464
result[10] = 0xE81A20F2023C2D0
result[11] = 0x2E41EAE69D89F186
result[12] = 0x425C831DD2A3E5FD
result[13] = 0x82788DBBDC4100EC
result[14] = 0x6D0FEE8D3901DD20
result[15] = 0xEBE82A0A41E5D783
result[16] = 0x2AFA26414B72E506
result[17] = 0xD1848E9C21D114D

chars = string.printable.encode()
flag = b'DH{'

for i in range(1, 9):
    hash_result = p64(result[i * 2]) + p64(result[i * 2 + 1])

    for char1 in chars:
        for char2 in chars:
            for char3 in chars:
                found = False

                tmp = bytes([char1]) + bytes([char2]) + bytes([char3])
                if hashlib.md5(tmp).digest() == hash_result:
                    flag += tmp
                    found = True
                    break

            if found == True:
                break
            
        if found == True:
            break

    print(flag)
```

```
$ python3 solve.py
b'DH{m-d'
b'DH{m-d-5_'
b'DH{m-d-5_1s_'
b'DH{m-d-5_1s_vu1'
b'DH{m-d-5_1s_vu1n-e'
b'DH{m-d-5_1s_vu1n-er-4'
b'DH{m-d-5_1s_vu1n-er-4b1e'
b'DH{m-d-5_1s_vu1n-er-4b1e~!}'
```