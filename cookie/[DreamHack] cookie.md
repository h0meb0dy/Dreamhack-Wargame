# [DreamHack] cookie

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 쿠키로 인증 상태를 관리하는 간단한 로그인 서비스입니다.
> admin 계정으로 로그인에 성공하면 플래그를 획득할 수 있습니다.
>
> Release: [cookie.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8551197/cookie.zip)

## Analysis

### index()

```python
@app.route('/')
def index():
    username = request.cookies.get('username', None) # username 변수를 'username' 쿠키의 값으로 설정
    if username:
        return render_template('index.html', text=f'Hello {username}, {"flag is " + FLAG if username == "admin" else "you are not admin"}') # username이 'admin'일 경우 플래그를 출력, 그렇지 않을 경우 'you are not admin'을 출력
    return render_template('index.html')
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
            pw = users[username] # 입력받은 username이 users에 있으면 (username이 'guest' 또는 'admin'이면) pw를 users[username]으로 설정
        except:
            return '<script>alert("not found user");history.go(-1);</script>' # username이 users에 없으면 "not found user" 창을 띄우고 이전 페이지로 돌아감
        if pw == password: # username에 대한 password를 맞게 입력했다면
            resp = make_response(redirect(url_for('index')) )
            resp.set_cookie('username', username) # 'username' 쿠키의 값을 username으로 설정해서 index 페이지를 반환함
            return resp 
        return '<script>alert("wrong password");history.go(-1);</script>' # password가 틀리면 "wrong password" 창을 띄우고 이전 페이지로 돌아감
```

## Exploit

`/` 페이지에 접속할 때 `'username'` 쿠키의 값이 `'admin'`이기만 하면 되기 때문에 직접 쿠키를 수정해서 요청을 보내면 플래그를 획득할 수 있다.

![image](https://user-images.githubusercontent.com/102066383/162609536-fbaaa32d-6237-44c8-a828-cff42e2078ea.png)

쿠키를 설정하고 새로고침을 하면

![image](https://user-images.githubusercontent.com/102066383/162609550-9c4a1043-6903-48d4-b4f3-a13d5dcb5145.png)

`admin`으로 로그인한 것처럼 플래그를 얻을 수 있다.

```
flag: DH{7952074b69ee388ab45432737f9b0c56}
```