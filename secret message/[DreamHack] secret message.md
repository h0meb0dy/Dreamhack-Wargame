# [DreamHack] secret message

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 드림이는 비밀스런 이미지 파일을 자신이 공부한 알고리즘을 통해 인코딩 하였어요.
>
> 인코딩 프로그램을 분석하여 원본 이미지를 알아내주세요.
>
> 원본 파일을 구한 경우 imageviewer.py를 통해 이미지를 볼 수 있습니다.
>
> Release: [secret message.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8596386/secret.message.zip)

## Analysis

### main()

```c
__int64 __fastcall main(int argc, char **argv, char **envp)
{
  FILE *original_file; // [rsp+0h] [rbp-10h]
  FILE *encoded_file; // [rsp+8h] [rbp-8h]

  original_file = fopen("secretMessage.raw", "rb");
  encoded_file = fopen("secretMessage.enc", "wb");
  encode(original_file, encoded_file);
  remove("secretMessage.raw");
  puts("done!");
  fclose(encoded_file);
  fclose(original_file);
  return 0LL;
}
```

`secretMessage.raw` 파일을 `secretMessage.enc` 파일로 인코딩하는 프로그램이다. `encode()` 함수 내부에서 인코딩이 이루어진다.

### encode()

```c
__int64 __fastcall encode(FILE *original_file, FILE *encoded_file)
{
  unsigned __int8 count; // [rsp+17h] [rbp-9h]
  int original_char; // [rsp+18h] [rbp-8h]
  int original_prev_char; // [rsp+1Ch] [rbp-4h]

  if ( original_file && encoded_file )
  {
    original_prev_char = 0xFFFFFFFF;
    count = 0;
    while ( 1 )
    {
      original_char = fgetc(original_file);
      if ( original_char == 0xFFFFFFFF )
        return 0LL;
      fputc(original_char, encoded_file);
      if ( original_char == original_prev_char )
      {
        count = 0;
        while ( 1 )
        {
          original_char = fgetc(original_file);
          if ( original_char == 0xFFFFFFFF )
            break;
          if ( original_char != original_prev_char )
          {
            fputc(count, encoded_file);
            fputc(original_char, encoded_file);
            original_prev_char = original_char;
            break;
          }
          if ( ++count == 0xFF )
          {
            fputc(0xFF, encoded_file);
            original_prev_char = 0xFFFFFFFF;
            break;
          }
        }
      }
      else
      {
        original_prev_char = original_char;
      }
      if ( original_char == 0xFFFFFFFF )
      {
        fputc(count, encoded_file);
        return 0LL;
      }
    }
  }
  else
  {
    *__errno_location() = 2;
    return 0xFFFFFFFFLL;
  }
}
```

`original_file`에서 한 글자씩 읽으면서 다음의 동작을 수행한다.

- 읽어온 글자를 `encoded_file`에 쓴다.
- 읽어온 글자가 바로 이전에 읽어온 글자와 같으면
  - `count`를 0으로 초기화한다.
  - 한 글자를 더 읽어온다. 읽어올 글자가 없으면 반복문을 빠져나가서, `encoded_file`에 `count`를 쓰고 리턴한다.
  - 읽어온 글자가 바로 이전에 읽어온 글자와 다르면, `encoded_file`에 `count`와 지금 읽어온 글자를 연속해서 쓰고, 반복문을 빠져나간다.
  - 읽어온 글자가 바로 이전에 읽어온 글자와 또 같으면, `count`를 1 증가시킨다. `count`가 `0xff`가 되면 `encoded_file`에 `count`를 쓰고 반복문을 빠져나간다. `original_prev_char`는 -1이 된다.

## Solve

### Idea

인코딩된 파일의 내용을 한 글자씩 읽으면서, 다음의 과정을 거쳐 원래의 파일을 복구할 수 있다.

- `encoded_file`과 `original_file`의 첫 번째 글자는 같다.
  ```python
      if idx == 0:
          original_file_content += bytes([encoded_file_content[idx]])
  ```
- n번째 글자와 (n+1)번째 글자가 다르면, `original_file`에 그 두 글자를 그대로 쓴다.
  ```
      elif encoded_file_content[idx] != encoded_file_content[idx - 1]:
          original_file_content += bytes([encoded_file_content[idx]])
- n번째 글자와 (n+1)번째 글자가 같으면, `original_file`에 그 글자를 두 번 연속으로 쓴다.
  - 이 경우, (n+2)번째 글자는 무조건 `count`에 해당한다. `count`는 그 글자가 몇 번이나 더 반복되었는지를 의미하는 것이므로, `original_file`에 n번째 글자를 `count` 번 연속으로 쓴다.
  - (n+3)번째 글자가 있다면 바로 다음에 쓴다.
    ```python
        elif encoded_file_content[idx] == encoded_file_content[idx - 1]:
            original_file_content += bytes([encoded_file_content[idx]])
            count = encoded_file_content[idx + 1]
            original_file_content += bytes([encoded_file_content[idx]]) * count
            idx += 1
            
            if idx + 1 < encoded_file_len:
                idx += 1
                original_file_content += bytes([encoded_file_content[idx]])
    ```
  

### Full code

```python
encoded_file_name = './release/secretMessage.enc'
encoded_file = open(encoded_file_name, 'rb')
encoded_file_content = encoded_file.read()
encoded_file_len = len(encoded_file_content)
encoded_file.close()

original_file_content = b''

idx = 0

while 1:
    if idx >= encoded_file_len:
        break

    if idx == 0:
        original_file_content += bytes([encoded_file_content[idx]])

    elif encoded_file_content[idx] == encoded_file_content[idx - 1]:
        original_file_content += bytes([encoded_file_content[idx]])
        count = encoded_file_content[idx + 1]
        original_file_content += bytes([encoded_file_content[idx]]) * count
        idx += 1
        
        if idx + 1 < encoded_file_len:
            idx += 1
            original_file_content += bytes([encoded_file_content[idx]])

    elif encoded_file_content[idx] != encoded_file_content[idx - 1]:
        original_file_content += bytes([encoded_file_content[idx]])

    idx += 1


original_file_name = 'secretMessage.raw'
original_file = open(original_file_name, 'wb')
original_file.write(original_file_content)
original_file.close()
```

```
$ python3 solve.py; python3 imageviewer.py secretMessage.raw
```

![image](https://user-images.githubusercontent.com/104156058/166117420-132e920c-e9ab-4bf0-85be-2ab1a6da7283.png)

```
flag: DH{93589e6c1db065fa95075ab5e3790bc1}
```