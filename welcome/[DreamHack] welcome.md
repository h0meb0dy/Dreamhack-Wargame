# [DreamHack] welcome

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 서버에서 작동하고 있는 서비스(welcome)의 바이너리와 소스 코드가 주어집니다.
> "접속 정보 보기"를 눌러 서비스 정보를 얻은 후 플래그를 획득하세요.
> 서버로부터 얻은 플래그의 내용을 워게임 사이트에 인증하면 점수를 획득할 수 있습니다.
> 플래그의 형식은 DH{…} 입니다.
>
> Release: [welcome.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8556092/welcome.zip)

## Mitigation

![image](https://user-images.githubusercontent.com/102066383/162667033-5fe42896-c322-4a3b-9ee8-10b7ef098501.png)

## Analysis

```c
int main(void) {
    
    FILE *fp;
    char buf[0x80] = {};
    size_t flag_len = 0;

    printf("Welcome To DreamHack Wargame!\n");

    fp = fopen("/flag", "r");
    fseek(fp, 0, SEEK_END);
    flag_len = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    fread(buf, 1, flag_len, fp);
    fclose(fp);

    printf("FLAG : ");

    fwrite(buf, 1, flag_len, stdout);
}
```

그냥 서버에 접속하면 플래그를 준다.

## Exploit

```
$ nc host1.dreamhack.games 15555
Welcome To DreamHack Wargame!
FLAG : DH{5cc72596cba7104569abb37f71b8ccf3}
```