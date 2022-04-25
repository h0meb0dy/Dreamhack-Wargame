# [DreamHack] csrf-2

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 여러 기능과 입력받은 URL을 확인하는 봇이 구현된 서비스입니다.
>
> CSRF 취약점을 이용해 플래그를 획득하세요.
>
> Release: [csrf-2.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8551339/csrf-2.zip)

## Analysis

### /

```python
@app.route("/")
def index():
    session_id = request.cookies.get('sessionid', None)
    try:
        username = session_storage[session_id] # 'sessionid' 쿠키의 값으로 이용자를 식별
    except KeyError:
        return render_template('index.html', text='please login') # session_id가 session_storage에 없을 경우 'please login' 출력

    return render_template('index.html', text=f'Hello {username}, {"flag is " + FLAG if username == "admin" else "you are not an admin"}') # 'admin'으로 로그인하면 플래그 출력, 그렇지 않으면 'you are not an admin' 출력
```

admin으로 로그인하면 플래그를 획득할 수 있다.

### /vuln

```python
@app.route("/vuln")
def vuln():
    param = request.args.get("param", "").lower() # 대소문자를 혼용하여 필터링을 우회하는 공격 방지
    xss_filter = ["frame", "script", "on"]
    for _ in xss_filter:
        param = param.replace(_, "*") # 악성 스크립트 삽입 방지
    return param
```

이용자가 입력한 `param`을 그대로 출력하여 XSS 취약점이 발생한다.

### /flag

```python
@app.route("/flag", methods=["GET", "POST"])
def flag():
    if request.method == "GET":
        return render_template("flag.html")
    elif request.method == "POST":
        param = request.form.get("param", "")
        session_id = os.urandom(16).hex()
        session_storage[session_id] = 'admin' # session_storage에 admin 추가
        if not check_csrf(param, {"name":"sessionid", "value": session_id}): # 서버에서 'sessionid' 쿠키의 값을 admin의 session_id로 설정해서 /vuln?param=<param>으로 접속 요청
            return '<script>alert("wrong??");history.go(-1);</script>'

        return '<script>alert("good");history.go(-1);</script>'
```

서버에서 `'sessionid'` 쿠키를 admin의 `session_id`로 설정해서 `/vuln?param=<param>`으로 접속 요청을 보낸다.

### /login

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            pw = users[username] # 입력받은 username을 users에서 검색
        except:
            return '<script>alert("not found user");history.go(-1);</script>'
        if pw == password: # 입력받은 password를 users의 pw와 비교
            resp = make_response(redirect(url_for('index')) )
            session_id = os.urandom(8).hex()
            session_storage[session_id] = username # session_storage에 username 추가
            resp.set_cookie('sessionid', session_id) # 로그인에 성공하면 'sessionid' 쿠키를 session_id로 설정
            return resp 
        return '<script>alert("wrong password");history.go(-1);</script>'
```

### /change_password

```python
@app.route("/change_password")
def change_password():
    pw = request.args.get("pw", "")
    session_id = request.cookies.get('sessionid', None)
    try:
        username = session_storage[session_id]
    except KeyError:
        return render_template('index.html', text='please login') # session_id가 session_storage에 없을 경우 'please login' 출력

    users[username] = pw # users에 저장된 비밀번호 변경
    return 'Done'
```

## Exploit

![image](https://user-images.githubusercontent.com/102066383/163458250-88eab3c1-e879-4559-ab93-242502a04644.png)

`/flag`의 `param`에 `<img src="/change_password?pw=aaaa">`를 넣고 제출하면 admin의 비밀번호가 `aaaa`로 바뀐다.

![image](https://user-images.githubusercontent.com/102066383/163458374-cfc208fb-fd08-4199-afca-728e95ce16d2.png)

`admin / aaaa`로 로그인하면

![image](https://user-images.githubusercontent.com/102066383/163458450-0e5d3eb3-fcec-4b34-859d-c5857805b4d9.png)

플래그를 획득할 수 있다.

```
flag: DH{c57d0dc12bb9ff023faf9a0e2b49e470a77271ef}
```
