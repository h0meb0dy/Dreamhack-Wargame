# [DreamHack] baseball

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 바이너리를 분석하여 플래그를 얻어주세요.
> 얻은 플래그는 `DH{<flag>}` 형식으로 인증해주세요.
>
> Release: [baseball.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8598526/baseball.zip)

## Analysis

### main()

```c
  table_fp = fopen(argv[1], "rb");
  if ( !table_fp )
  {
    fwrite("File not found\n", 1uLL, 0xFuLL, stderr);
    exit(-1);
  }
  fseek(table_fp, 0LL, 2);
  table_len = ftell(table_fp);
  fseek(table_fp, 0LL, 0);
  if ( table_len != 64 )
  {
    fwrite("Invalid table\n", 1uLL, 0xEuLL, stderr);
    exit(-1);
  }
  fread(&table, 0x41uLL, 1uLL, table_fp);
  fclose(table_fp);
```

Table file로부터 table을 읽어온다. 테이블의 길이는 64바이트여야 한다.

```c
  input_fp = fopen(argv[2], "rb");
  if ( !input_fp )
  {
    fwrite("File not found\n", 1uLL, 0xFuLL, stderr);
    exit(-1);
  }
  fseek(input_fp, 0LL, 2);
  input_len = ftell(input_fp);
  if ( !input_len )
  {
    fwrite("Invalid input\n", 1uLL, 0xEuLL, stderr);
    exit(-1);
  }
  fseek(input_fp, 0LL, 0);
  input = malloc(input_len + 1);
  if ( !input )
  {
    fwrite("Allocation failed\n", 1uLL, 0x12uLL, stderr);
    exit(-1);
  }
  memset(input, 0, input_len + 1);
  fread(input, input_len, 1uLL, input_fp);
  fclose(input_fp);
```

Input file로부터 input을 읽어온다.

```c
  output = (char *)encode(input, (unsigned int)input_len);
  printf("%s", output);
```

읽어온 `input`을 `encode()`에 넣어서 `output`을 만들고, 출력한다.

### encode()

```c
  while ( input_end - input_cur > 2 )
  {
    *output_cur = table[*input_cur >> 2];
    output_cur[1] = table[(input_cur[1] >> 4) | (16 * *input_cur) & 0x30];
    output_cur[2] = table[(input_cur[2] >> 6) | (4 * input_cur[1]) & 0x3C];
    v3 = output_cur + 3;
    output_cur += 4;
    *v3 = table[input_cur[2] & 0x3F];
    input_cur += 3;
  }
```

`input`의 3바이트를 `output`의 4바이트로 인코딩하고, 이 과정을 `input`에 남은 문자가 2바이트 이하가 될 때까지 반복한다. 인코딩 과정을 보면 `input`과 `output`을 알 때 역연산을 통해 `table`을 알아낼 수 있다.

```c
  if ( input_end != input_cur )
  {
    v4 = output_cur;
    v9 = output_cur + 1;
    *v4 = table[*input_cur >> 2];
    if ( input_end - input_cur == 1 )
    {
      *v9 = table[(16 * *input_cur) & 0x30];
      v5 = v9 + 1;
      v10 = v9 + 2;
      *v5 = '=';
    }
    else
    {
      *v9 = table[(input_cur[1] >> 4) | (16 * *input_cur) & 0x30];
      v6 = v9 + 1;
      v10 = v9 + 2;
      *v6 = table[(4 * input_cur[1]) & 0x3C];
    }
    v7 = v10;
    output_cur = v10 + 1;
    *v7 = '=';
  }
```

`input`의 마지막 1바이트 또는 2바이트의 경우 살짝 다른 방식으로 인코딩한다. 이 경우들도 마찬가지로 역연산을 구현할 수 있다.

## Solve

### Find table

문제에서 주어진 `text_in.txt`와 `text_out.txt`를 통해 table을 알아낼 수 있다.

```python
# find table

text_in_file = open('text_in.txt', 'rb')
text_in = text_in_file.read()
text_in_file.close()

text_out_file = open('text_out.txt', 'rb')
text_out = text_out_file.read()
text_out_file.close()

table_arr = [0 for i in range(64)]

for i in range(int(len(text_in) / 3)):
    table_arr[text_in[i * 3] >> 2] = text_out[i * 4]
    table_arr[(text_in[i * 3 + 1] >> 4) | (text_in[i * 3] * 16) & 0x30] = text_out[i * 4 + 1]
    table_arr[(text_in[i * 3 + 2] >> 6) | (text_in[i * 3 + 1] * 4) & 0x3c] = text_out[i * 4 + 2]
    table_arr[text_in[i * 3 + 2] & 0x3f] = text_out[i * 4 + 3]

i += 1

table_arr[text_in[i * 3] >> 2] = text_out[i * 4]

if len(text_in) % 3 == 1:
    table_arr[(text_in[i * 3] * 16) & 0x30] = text_out[i * 4 + 1]
elif len(text_in) % 3 == 2:
    table_arr[(text_in[i * 3 + 1] >> 4) | (text_in[i * 3] * 16) & 0x30] = text_out[i * 4 + 1]
    table_arr[(text_in[i * 3 + 1] * 4) & 0x3c]

table = b''
for t in table_arr:
    table += bytes([t])

table_file = open('table.txt', 'wb')
table_file.write(table)
table_file.close()
```

알아낸 `table.txt` 파일로 `text_in.txt`를 다시 인코딩해보면

```
$ ./baseball
$ ./baseball table.txt text_in.txt
7/OkZQIau/jou/R1by9acyjjutd0cUdlWshecQhkZUn1cUH1by9g4/9qNAn1byGaby9pbQSjWshgbUmqZAF+JtOBZUn1b8e1YoMPYoM1ny95ZAO+J/jaNAOB2vhrNLhVNDO0cshWNDIjbnrnZQhj4AM1S/Fmu/jou/GjN/n1bUm5JUFpNte1NyH1VA9yZUqLZQu13VR=
```

`text_out.txt`와 같은 결과를 얻는다. 올바른 table을 알아냈음을 확인할 수 있다.

### Find flag

`table.txt`를 이용하여 `flag_out.txt`를 디코딩하면 플래그를 획득할 수 있다.

```python
# find flag

table_file = open('table.txt', 'rb')
table = table_file.read()
table_file.close()

flag_out_file = open('flag_out.txt', 'rb')
flag_out = flag_out_file.read()
flag_out_file.close()

flag = b''

for i in range(int(len(flag_out) / 4) - 1):
    flag_arr = [0, 0, 0] # flag[i * 3] ~ flag[i * 3 + 2]

    flag_arr[0] += table.index(flag_out[i * 4]) << 2
    flag_arr[0] += (table.index(flag_out[i * 4 + 1]) & 0x30) >> 4
    flag_arr[1] += (table.index(flag_out[i * 4 + 1]) & 0xf) << 4
    flag_arr[1] += (table.index(flag_out[i * 4 + 2]) & 0x3c) >> 2
    flag_arr[2] += (table.index(flag_out[i * 4 + 2]) & 0x3) << 6
    flag_arr[2] += table.index(flag_out[i * 4 + 3])

    flag += bytes([flag_arr[0]])
    flag += bytes([flag_arr[1]])
    flag += bytes([flag_arr[2]])

i += 1

flag_arr = [0, 0, 0] # flag[-3] ~ flag[-1]

flag_arr[0] += table.index(flag_out[i * 4]) << 2

if flag_out[i * 4 + 3] != ord(b'='): # len(flag) % 3 == 0
    flag_arr[0] += (table.index(flag_out[i * 4 + 1]) & 0x30) >> 4
    flag_arr[1] += (table.index(flag_out[i * 4 + 1]) & 0xf) << 4
    flag_arr[1] += (table.index(flag_out[i * 4 + 2]) & 0x3c) >> 2
    flag_arr[2] += (table.index(flag_out[i * 4 + 2]) & 0x3) << 6
    flag_arr[2] += table.index(flag_out[i * 4 + 3])
elif flag_out[i * 4 + 2] != ord(b'='): # len(flag) % 3 == 2
    flag_arr[0] += (table.index(flag_out[i * 4 + 1]) & 0x30) >> 4
    flag_arr[1] += (table.index(flag_out[i * 4 + 1]) & 0xf) << 4
    flag_arr[1] += table.index(flag_out[i * 4 + 2]) >> 2
else: # len(flag) % 3 == 1
    flag_arr[0] += table.index(flag_out[i * 4 + 1]) >> 4

flag += bytes([flag_arr[0]])
flag += bytes([flag_arr[1]])
flag += bytes([flag_arr[2]])

print(flag)
```

```
$ python3 solve.py
b'Did you know how base64 works\x00'
```

알아낸 플래그를 다시 인코딩해보면

```
$ ./baseball table.txt flag.txt
S/jeutjaJvhlNA9Du/GaJBhLbQdjd+n1Jy9BcD3=
```

`flag_out.txt`와 같은 결과를 얻는다.

```
flag: DH{Did you know how base64 works}
```