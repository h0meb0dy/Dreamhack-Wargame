# [DreamHack] csrf-1

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 여러 기능과 입력받은 URL을 확인하는 봇이 구현된 서비스입니다.
>
> CSRF 취약점을 이용해 플래그를 획득하세요.
>
> Release: [csrf-1.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8551509/csrf-1.zip)

## Analysis

### /vuln

```python
@app.route("/vuln")
def vuln():
    param = request.args.get("param", "").lower() # 대소문자를 혼용해서 필터링을 우회하는 공격 방지
    xss_filter = ["frame", "script", "on"]
    for _ in xss_filter:
        param = param.replace(_, "*") # 악성 스크립트 삽입 방지
    return param
```

이용자가 입력한 `param`을 그대로 출력해서 XSS 취약점이 발생한다. 

### /flag

```python
@app.route("/flag", methods=["GET", "POST"])
def flag():
    if request.method == "GET":
        return render_template("flag.html")
    elif request.method == "POST":
        param = request.form.get("param", "")
        if not check_csrf(param):
            return '<script>alert("wrong??");history.go(-1);</script>'

        return '<script>alert("good");history.go(-1);</script>'
```

이용자가 입력한 `param`을 인자로 `check_csrf()`를 호출한다. `check_csrf()`는 내부에서 `read_url()`을 호출하여 서버에서 `/vuln?param=<param>`으로 요청을 보낸다.

### /admin/notice_flag

```python
@app.route("/admin/notice_flag")
def admin_notice_flag():
    global memo_text
    if request.remote_addr != "127.0.0.1":
        return "Access Denied"
    if request.args.get("userid", "") != "admin":
        return "Access Denied 2"
    memo_text += f"[Notice] flag is {FLAG}\n"
    return "Ok"
```

`127.0.0.1`에서 `/admin/notice_flag?userid=admin`으로 접속하면 `memo_text`에 플래그가 추가되어 `/memo`로 접속하면 플래그를 획득할 수 있다.

## Exploit

`<img>` 태그의 `src` 속성에 `/admin/notice_flag?userid=admin`을 넣어서 `/flag`의 `param`에 넣으면, 서버에서 이 주소로 접속 요청을 보내게 된다.

![image](https://user-images.githubusercontent.com/102066383/163453498-f9402f42-c9cb-4ba2-ba5f-049a0d585d92.png)

`param` 칸에 `<img src="/admin/notice_flag?userid=admin">`을 넣고 제출하면, `/memo`에 플래그가 저장되어 있다.

![image](https://user-images.githubusercontent.com/102066383/163453238-c4eed3b9-fa66-4055-b2f7-e887a2f4a061.png)

```
flag: DH{11a230801ad0b80d52b996cbe203e83d}
```