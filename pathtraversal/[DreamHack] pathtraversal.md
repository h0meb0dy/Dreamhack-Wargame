# [DreamHack] pathtraversal

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 사용자의 정보를 조회하는 API 서버입니다.
> Path Traversal 취약점을 이용해 `/api/flag`에 있는 플래그를 획득하세요!
>
> Release: [pathtraversal.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8598440/pathtraversal.zip)

## Analysis

### /api

```python
@app.route('/api')
@internal_api
def api():
    return '/user/<uid>, /flag'

@app.route('/api/user/<uid>')
@internal_api
def get_flag(uid):
    try:
        info = users[uid]
    except:
        info = {}
    return json.dumps(info)

@app.route('/api/flag')
@internal_api
def flag():
    return FLAG
```

`/api`는 `@internal_api`로 설정되어 있어 외부에서 접근하면 Unauthorized가 뜬다. 서버에서 `/api/flag`로 접속 요청을 보내도록 하면 플래그를 획득할 수 있다.

### /get_info

```python
@app.route('/get_info', methods=['GET', 'POST'])
def get_info():
    if request.method == 'GET':
        return render_template('get_info.html')
    elif request.method == 'POST':
        userid = request.form.get('userid', '')
        info = requests.get(f'{API_HOST}/api/user/{userid}').text
        return render_template('get_info.html', info=info)
```

`userid`에 값을 전달하면 서버에서 `/api/user/{userid}`로 접속 요청을 보낸다. `userid`에 `../flag`를 입력하면 URL은 `/api/user/../flag`가 되어, 결과적으로 `/api/flag`가 된다.

## Exploit

`userid`에 guest를 넣고 View를 누르면

![image](https://user-images.githubusercontent.com/104156058/166137114-91591e54-0a3e-41d6-bfcf-3020132572c6.png)

`userid`에 0이 전달된다. 이 값을 `../flag`로 바꿔서 보내면

![image](https://user-images.githubusercontent.com/104156058/166137128-4447cb77-2b8e-4b20-9694-967447e6d309.png)

![image](https://user-images.githubusercontent.com/104156058/166137137-2adff3f4-c865-447f-a912-cb27615012b9.png)

플래그를 획득할 수 있다.

```
flag: DH{8a33bb6fe0a37522bdc8adb65116b2d4}
```