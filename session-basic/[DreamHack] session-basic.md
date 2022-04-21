# [DreamHack] session-basic

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 쿠키와 세션으로 인증 상태를 관리하는 간단한 로그인 서비스입니다.
> admin 계정으로 로그인에 성공하면 플래그를 획득할 수 있습니다.
>
> Release: [session-basic.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8532726/session-basic.zip)

## Analysis

### users

```python
users = {
    'guest': 'guest',
    'user': 'user1234',
    'admin': FLAG
}
```

### index()

```python
@app.route('/')
def index():
    session_id = request.cookies.get('sessionid', None) # 'sessionid' 쿠키의 값을 session_id에 저장
    try:
        # get username from session_storage 
        username = session_storage[session_id] # session_storage의 key 중 session_id가 존재하면 username에 session_storage[session_id]를 저장
    except KeyError:
        return render_template('index.html')

    return render_template('index.html', text=f'Hello {username}, {"flag is " + FLAG if username == "admin" else "you are not admin"}') # username이 'admin'이면 플래그를 출력, 그렇지 않으면 'you are not admin'을 출력
```

### login()

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username') # username 입력
        password = request.form.get('password') # password 입력
        try:
            # you cannot know admin's pw 
            pw = users[username] # users의 key 중 username이 존재하면 pw에 users[username]을 저장
        except:
            return '<script>alert("not found user");history.go(-1);</script>' # users에 username이 존재하지 않으면 'not found user' 창을 띄우고 이전 페이지로 돌아감
        if pw == password: # username에 해당하는 password를 맞게 입력했다면
            resp = make_response(redirect(url_for('index')) )
            session_id = os.urandom(32).hex() # 32바이트 길이의 random한 session_id 생성
            session_storage[session_id] = username # session_storage에 {session_id: username} 쌍 추가
            resp.set_cookie('sessionid', session_id) # 'sessionid' 쿠키의 값을 session_id로 설정
            return resp # index 페이지를 반환
        return '<script>alert("wrong password");history.go(-1);</script>' # password가 맞지 않으면 'wrong password' 창을 띄우고 이전 페이지로 돌아감
```

### admin()

```python
@app.route('/admin')
def admin():
    # what is it? Does this page tell you session? 
    # It is weird... TODO: the developer should add a routine for checking privilege 
    return session_storage # /admin으로 접속하면 session_storage를 볼 수 있음
```

### main

```python
if __name__ == '__main__':
    import os
    # create admin sessionid and save it to our storage
    # and also you cannot reveal admin's sesseionid by brute forcing!!! haha
    session_storage[os.urandom(32).hex()] = 'admin' # admin의 session_id는 미리 설정되어 있음
    print(session_storage)
    app.run(host='0.0.0.0', port=8000)
```

## Exploit

서비스가 시작될 때 `admin`의 `session_id`는 미리 설정되어 있다. `/admin`으로 접속하면 `session_storage`를 볼 수 있으므로 `admin`의 `session_id`를 얻을 수 있다. 이 값을 `/` 페이지에서 `'sessionid'` 쿠키에 설정하면 `username`이 `'admin'`이 되어 플래그를 획득할 수 있다.

![image](https://user-images.githubusercontent.com/102066383/162609951-300353d8-3325-4549-b109-7c477ce6ba1b.png)

`/admin`에 접속해서 얻은 `'admin'`의 `session_id`는 `6862eb9d30d92e22f7b190dd3f801fff6484c28c53574c4c108c0d649ef39666`이다.

![image](https://user-images.githubusercontent.com/102066383/162610006-5e548494-19ef-4f5b-9c93-98a6832b57e2.png)

`index` 페이지에서 `sessionid`를 이 값으로 설정하고 새로고침을 하면

![image](https://user-images.githubusercontent.com/102066383/162610016-5763725f-4129-4a92-a50d-13986d779836.png)

플래그를 획득할 수 있다.

```
flag: DH{8f3d86d1134c26fedf7c4c3ecd563aae3da98d5c}
```
