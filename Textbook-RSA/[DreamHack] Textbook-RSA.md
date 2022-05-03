# [DreamHack] Textbook-RSA

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 드림이가 비밀 플래그를 가지고 있는 RSA 서버를 운영하고 있습니다. 서버를 공격해 플래그를 탈취해주세요!
>
> Release: [Textbook-RSA.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8606125/Textbook-RSA.zip)

## Analysis

```python
class RSA(object):
    def __init__(self):
        self.p = getStrongPrime(512)
        self.q = getStrongPrime(512)
        self.N = self.p * self.q
        self.e = 0x10001
        self.d = inverse(self.e, self.N - self.p - self.q + 1)

    def encrypt(self, pt):
        return pow(pt, self.e, self.N)

    def decrypt(self, ct):
        return pow(ct, self.d, self.N)
```

두 소수 `p`와 `q`는 `getStrongPrime(512)`로 만들어지고, 공개키 `e`는 `0x10001`이다.

### Encrypt

```python
    if choice == "1":
        print("Input plaintext (hex): ", end="")
        pt = bytes_to_long(bytes.fromhex(input()))
        print(rsa.encrypt(pt))
```

평문을 16진수 문자열 형태로 입력받아서 암호화한다.

### Decrypt

```python
    elif choice == "2":
        print("Input ciphertext (hex): ", end="")
        ct = bytes_to_long(bytes.fromhex(input()))
        if ct == FLAG_enc or ct > rsa.N:
            print("Do not cheat !")
        else:
            print(rsa.decrypt(ct))
```

암호문을 16진수 문자열 형태로 입력받아서 복호화한다. 플래그의 암호문이나, `N`보다 큰 암호문은 입력할 수 없다.

### Get info

```python
    elif choice == "3":
        print(f"N: {rsa.N}")
        print(f"e: {rsa.e}")
        print(f"FLAG: {FLAG_enc}")
```

`N`과 `e`, 그리고 플래그의 암호문을 출력해준다.

## Solve

플래그를 제외한 모든 암호문을 복호화해볼 수 있기 때문에, 다음의 원리로 공격할 수 있다.
$$
flag\_enc=flag^e\ (mod\ n)\\
c=2^e\ (mod\ n)\\
flag\_enc\times c=(flag\times 2)^e\ (mod\ n)\\
$$
플래그의 암호문에 `02`의 암호문을 곱해서 복호화한 후, 그 결과를 2로 나누면 플래그를 얻을 수 있다.

```python
from pwn import *
from Crypto.Util.number import long_to_bytes
import binascii

r = remote('host1.dreamhack.games', 19484)

sla = r.sendlineafter

def encrypt(pt):
    sla(b'[3] Get info\n', b'1')
    sla(b'Input plaintext (hex): ', binascii.hexlify(long_to_bytes(pt)))
    return int(r.recvline()[:-1])

def decrypt(ct):
    sla(b'[3] Get info\n', b'2')
    sla(b'Input ciphertext (hex): ', binascii.hexlify(long_to_bytes(ct)))
    return int(r.recvline()[:-1])

def get_info():
    sla(b'[3] Get info\n', b'3')
    
    r.recvuntil(b'N: ')
    n = int(r.recvline()[:-1])

    r.recvuntil(b'e: ')
    e = int(r.recvline()[:-1])

    r.recvuntil(b'FLAG: ')
    flag_enc = int(r.recvline()[:-1])

    return n, e, flag_enc

n, e, flag_enc = get_info()
c = encrypt(2) # ciphertext of 0x02
flag_int = decrypt(flag_enc * c % n) >> 1
flag = long_to_bytes(flag_int)
print(flag)

r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 19484: Done
b'DH{6623c33be90cc27728d4ec7287785992}'
```