# [DreamHack] funjs

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 입력 폼에 데이터를 입력하여 맞으면 플래그, 틀리면 `NOP !`을 출력하는 HTML 페이지입니다.
> main 함수를 분석하여 올바른 입력 값을 찾아보세요 !
>
> Release: [funjs.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8596091/funjs.zip)

## Analysis

### index.html

![image](https://user-images.githubusercontent.com/104156058/166090733-c45da9a2-6183-43b7-a0f5-64f53fd4c624.png)

`index.html`을 브라우저에서 열어보면 위와 같은 입력 칸이 계속 움직이고 있다. 테스트할 때 상당히 귀찮으니, 코드 맨 위쪽의 `setInterval(moveBox,1000);`을 주석 처리하면 좋다.

```html
    <body>
        <div id='formbox'>
            <h2>Find FLAG !</h2>
            <input type='flag' id='flag' value=''>
            <input type='button' value='submit' onclick='main()'>
        </div>
    </body>
```

문자열을 입력하고 submit을 누르면 `main()`이 실행된다.

### main()

코드가 복잡해 보이는데, 맨 아래 부분만 보면 된다.

```javascript
        if (flag[_0x374fd6(0x17c)] != 0x24) {
            text2img(_0x374fd6(0x185));
            return;
        }
```

이 부분은 입력한 문자열의 길이를 검사하는 코드로 보인다. 문자열의 길이가 `0x24`가 아니면 `_0x374fd6(0x185)`를 출력하고 return하는데, 이 출력값은 플래그를 틀리게 입력해보면 `NOP!`임을 확인할 수 있다.

```javascript
        for (var i = 0x0; i < flag[_0x374fd6(0x17c)]; i++) {
            if (flag[_0x374fd6(0x176)](i) == operator[i % operator[_0x374fd6(0x17c)]](_0x4949[i], _0x42931[i])) {} else {
                text2img(_0x374fd6(0x185));
                return;
            }
        }
        text2img(flag);
```

이 부분은 플래그의 길이만큼 반복문을 돌면서, 한 글자씩 플래그와 일치하는지 검사하는 코드로 보인다. `if (flag[_0x374fd6(0x176)](i) == operator[i % operator[_0x374fd6(0x17c)]](_0x4949[i], _0x42931[i]))`라는 조건문을 통과하지 못하면 길이가 틀렸을 때와 마찬가지로 `_0x374fd6(0x185)`를 출력하고 return한다. 그렇다면 `operator[i % operator[_0x374fd6(0x17c)]](_0x4949[i], _0x42931[i])`라는 값을 모두 이어붙이면 플래그가 될 것이다.

입력한 문자열이 플래그와 같으면 `text2img(flag)`로 플래그를 출력한다.

## Exploit

앞에서 분석한 `main()`의 맨 아래쪽의 코드를 다음과 같이 수정한다.

```javascript
        /* if (flag[_0x374fd6(0x17c)] != 0x24) {
            text2img(_0x374fd6(0x185));
            return;
        } */
        var flag = ''
        for (var i = 0x0; i < 0x24; i++) {
            flag += String.fromCharCode(operator[i % operator[_0x374fd6(0x17c)]](_0x4949[i], _0x42931[i]));
            /* if (flag[_0x374fd6(0x176)](i) == operator[i % operator[_0x374fd6(0x17c)]](_0x4949[i], _0x42931[i])) {} else {
                text2img(_0x374fd6(0x185));
                return;
            } */
        }
        // text2img(flag);
        console.log(flag);
```

입력한 문자열의 길이를 검사하는 부분과, 플래그와 일치하는지 검사하는 부분을 모두 주석 처리하고, 대신 올바른 플래그를 구해서 콘솔에 출력하는 코드를 추가한다.

수정한 후 다시 `index.html`을 열어서 submit을 눌러보면

![image](https://user-images.githubusercontent.com/104156058/166091374-2137cfc8-da42-46f3-85c8-21d4fac506bb.png)

플래그를 획득할 수 있다.

```
flag: DH{cfd4a77a013ea616d3d5cc0ddf87c1ea}
```