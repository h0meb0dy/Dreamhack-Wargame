# [DreamHack] proxy-1

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Raw Socket Sender가 구현된 서비스입니다.
> 요구하는 조건을 맞춰 플래그를 획득하세요. 플래그는 flag.txt, FLAG 변수에 있습니다.
>
> Release: [proxy-1.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8554753/proxy-1.zip)

## Analysis

### /socket

```python
@app.route('/socket', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('socket.html')
    elif request.method == 'POST':
        host = request.form.get('host')
        port = request.form.get('port', type=int)
        data = request.form.get('data')

        retData = ""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect((host, port))
                s.sendall(data.encode())
                while True:
                    tmpData = s.recv(1024)
                    retData += tmpData.decode()
                    if not tmpData: break
            
        except Exception as e:
            return render_template('socket_result.html', data=e)
        
        return render_template('socket_result.html', data=retData)
```

Raw socket sender가 구현된 페이지이다. `host`, `port`, `data`를 입력하면 그 `host`와 `port`로 `data`를 전송한다.

### /admin

```python
@app.route('/admin', methods=['POST'])
def admin():
    if request.remote_addr != '127.0.0.1':
        return 'Only localhost'

    if request.headers.get('User-Agent') != 'Admin Browser':
        return 'Only Admin Browser'

    if request.headers.get('DreamhackUser') != 'admin':
        return 'Only Admin'

    if request.cookies.get('admin') != 'true':
        return 'Admin Cookie'

    if request.form.get('userid') != 'admin':
        return 'Admin id'

    return FLAG
```

`/admin`으로 보낸 요청이 다섯 가지 조건을 만족하면 플래그를 획득할 수 있다.

## Exploit

### Bypass 'Only localhost'

`request.remote_addr`이 127.0.0.1이려면 localhost에서 접속 요청을 보내야 한다. 코드를 보면 `app.run(host='0.0.0.0', port=8000)`으로 서버가 구동이 되므로, host에는 0.0.0.0을 넣고 port에는 8000을 넣어서 POST 요청을 보내면 정상적으로 응답을 받을 수 있다.

요청을 보낼 때는 POST content들을 위한 자리를 확보하기 위해 마지막에 개행을 두 번 추가해서 보내주어야 한다. 그렇지 않으면 timed out이 뜬다.

![image](https://user-images.githubusercontent.com/102066383/163781878-bd9ae60a-0a41-49a7-a7b5-ba70e6fbf78d.png)

![image](https://user-images.githubusercontent.com/102066383/163782129-a37aab60-59ac-466a-9386-08a71c05ef3a.png)

### Bypass 'Only Admin Browser'

HTTP 헤더의 `User-Agent`의 값이 `'Admin Browser'`여야 한다. `User-Agent` 헤더를 추가해서 요청을 보내면 된다.

![image](https://user-images.githubusercontent.com/102066383/163782278-adbf3e53-c81e-41ab-a1ab-52bf3084e1ec.png)

![image](https://user-images.githubusercontent.com/102066383/163782307-59452d4d-e53c-41b0-a269-c019992a6186.png)

### Bypass 'Only Admin'

HTTP 헤더의 `DreamhackUser`의 값이 `'admin'`이어야 한다. 마찬가지로 `DreamhackUser` 헤더를 추가해서 요청을 보내면 된다.

![image](https://user-images.githubusercontent.com/102066383/163782509-382ac8fe-f544-43c6-98d5-db7eb7317123.png)

![image](https://user-images.githubusercontent.com/102066383/163782695-547ac22c-6c8b-48c1-9b88-b035355d4a59.png)

### Bypass 'Admin Cookie'

`admin` 쿠키의 값이 `'true'`여야 한다. 서버에서 요청을 보내는 것이므로 클라이언트 브라우저에서 쿠키를 설정하면 안 되고, HTTP 헤더의 `Cookie` 필드에 `admin=true`를 넣어서 요청을 보내면 된다.

![image](https://user-images.githubusercontent.com/102066383/163783210-a0683f07-2476-4fc3-ac19-f93c6f7f3d69.png)

![image](https://user-images.githubusercontent.com/102066383/163783247-bc9035c1-a050-49c5-9162-93745c75a014.png)

### Bypass 'Admin id'

`userid` 변수에 `'admin'`을 전달해야 한다. 가장 밑의 content에 `userid=admin`을 쓰고, 이 데이터의 길이는 12바이트이므로 `Content-Length` 헤더에 12를 넣고, HTTP form 형태의 데이터이므로 `Content-Type` 헤더에 `application/x-www-form-urlencoded`를 넣어서 요청을 보내면 된다.

![image](https://user-images.githubusercontent.com/102066383/163796141-d621b13d-4eea-47d4-acc2-d71610c96d95.png)

![image](https://user-images.githubusercontent.com/102066383/163796153-7acec051-c235-492c-8914-b6d998a86fbb.png)

```
flag: DH{9bb7177b6267ff7288e24e06d8dd6df5}
```
