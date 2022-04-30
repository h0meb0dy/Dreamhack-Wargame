# [DreamHack] Secure Mail

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 중요한 정보가 적혀있는 보안 메일을 발견하였습니다.
>
> 보안 메일의 비밀번호는 생년월일 6자리인 것으로 파악되나, 저희는 비밀번호 정보를 가지고 있지 않습니다.
>
> 비밀번호를 알아내고 보안 메일을 읽어 중요한 정보를 알아내주세요!
>
> Release: [Secure Mail.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8596201/Secure.Mail.zip)

## Analysis

### Submit form

![image](https://user-images.githubusercontent.com/104156058/166093080-5d235f63-a83f-47ae-9d64-47b787213ac4.png)

```html
<input id="pass" type="password" maxlength="6" size=30 title="User password input" value="" placeholder="Input your birthday eg.) 850810">
<button type="submit" onclick="_0x9a220(pass.value);">Confirm</button>
```

6자리 숫자를 입력하고 Confirm을 누르면 `_0x9a220(pass.value)`를 실행한다.

###  \_0x9a220()

```javascript
function _0x9a220(_0x30bf04){var _0x540d50=_0x225843,_0x2ee89c=Array[_0x540d50('0x99','3itY')](_0x3eebe5(_0x30bf04,null,raw=!![]))[_0x540d50('0xe2','G(su')](_0x66324e=>_0x66324e['charCodeAt']()),_0x2fef58=new _0x58829a['_0x14c3a3'][(_0x540d50('0x29','d%09'))](_0x2ee89c,_0x2ee89c);file=[...],dfbora=_0x2fef58['decrypt'](file),odradurs1='';for(var _0x302add=0x0;_0x302add<dfbora[_0x540d50('0xde','@%wH')];_0x302add++)odradurs1+=String[_0x540d50('0x2','dARo')](dfbora[_0x302add]);if(_0x3eebe5(odradurs1,null,raw=!![])!=_0x540d50('0x55','dGZC'))return alert('Wrong'),![];return document['write'](_0x540d50('0x66','AZ$r')+odradurs1+'\x22>'),!![];}
```

입력한 패스워드가 틀리면 `alert('Wrong')`을 반환하고 맞으면 `document['write'](_0x540d50('0x66','AZ$r')+odradurs1+'\x22>')`을 반환하는데, 함수가 생긴 걸 보아하니 분석하려고 하기보다 브루트포싱을 하는 게 더 효율적일 것 같다.

## Exploit

```javascript
for (var year = 0; year <= 99; year++) {
    var result = 0;
    for (var month = 1; month <= 12; month++) {
        for (var day = 1; day <= 31; day++) {
            var pw = ''
            pw += String(year).padStart(2, '0');
            pw += String(month).padStart(2, '0');
            pw += String(day).padStart(2, '0');
            console.log(pw);
            result = _0x9a220(pw);
            if (result) {
                break;
            }
        }
        if (result) {
            break;
        }
    }
    if (result) {
        break;
    }
}
```

관리자 도구의 콘솔에서 위의 코드를 실행한다. `000101`부터 `991231`까지 차례로 `_0x9a220()`에 넣어보는 코드이다. 이때 함수가 `alert(Wrong)`을 반환하면 한 번 시도할 때마다 알림창이 떠서 귀찮기 때문에, 틀렸을 경우 0을, 맞았을 경우 1을 반환하도록 다음과 같이 코드를 수정한 후에 스크립트를 돌리면 된다.

```javascript
function _0x9a220(_0x30bf04){var _0x540d50=_0x225843,_0x2ee89c=Array[_0x540d50('0x99','3itY')](_0x3eebe5(_0x30bf04,null,raw=!![]))[_0x540d50('0xe2','G(su')](_0x66324e=>_0x66324e['charCodeAt']()),_0x2fef58=new _0x58829a['_0x14c3a3'][(_0x540d50('0x29','d%09'))](_0x2ee89c,_0x2ee89c);file=[...],dfbora=_0x2fef58['decrypt'](file),odradurs1='';for(var _0x302add=0x0;_0x302add<dfbora[_0x540d50('0xde','@%wH')];_0x302add++)odradurs1+=String[_0x540d50('0x2','dARo')](dfbora[_0x302add]);if(_0x3eebe5(odradurs1,null,raw=!![])!=_0x540d50('0x55','dGZC'))return 0;return 1;}
```

![image](https://user-images.githubusercontent.com/104156058/166096207-f2e895a7-89a4-4bdd-b260-25bdda146dd4.png)

960229에서 멈춘다. 반환값이 수정되지 않은 원래의 `secure-mail.html`에 다시 960229를 넣어보면

![image](https://user-images.githubusercontent.com/104156058/166096232-a168deb9-46b5-4722-ba34-20a19e816c57.png)

플래그를 획득할 수 있다.

```
flag: DH{Brutef0rce_th3_secur3_mail}
```