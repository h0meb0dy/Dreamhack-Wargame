# [DreamHack] [wargame.kr] strcmp

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> if you can bypass the strcmp function, you get the flag.

## Analysis

```php+HTML
<?php
    require("./lib.php"); // for FLAG

    $password = sha1(md5(rand().rand().rand()).rand());

    if (isset($_GET['view-source'])) {
        show_source(__FILE__);
        exit();
    }else if(isset($_POST['password'])){
        sleep(1); // do not brute force!
        if (strcmp($_POST['password'], $password) == 0) {
            echo "Congratulations! Flag is <b>" . $FLAG ."</b>";
            exit();
        } else {
            echo "Wrong password..";
        }
    }

?>
<br />
<br />
<form method="POST">
    password : <input type="text" name="password" /> <input type="submit" value="chk">
</form>
<br />
<a href="?view-source">view-source</a>
```

입력한 패스워드와 랜덤한 sha1 해쉬 값인 `$password`를 `strcmp()`로 비교했을 때 0을 반환하면 플래그를 준다.

그런데 `strcmp()`의 반환값과 0을 느슨한 비교로 체크하기 때문에 `strcmp()`가 0이 아니라 `NULL`을 반환해도 조건은 참이 된다.

PHP 5.3 이상 버전부터는 `strcmp()`로 배열과 문자열을 비교하면 `NULL`을 반환한다. 이를 이용하여 플래그를 획득할 수 있다.

## Exploit

패스워드를 입력하고 패킷을 잡아보면 다음과 같다.

![image](https://user-images.githubusercontent.com/102066383/163725937-4f23b50e-f07f-4c0c-8192-05d9f4ca642b.png)

패스워드를 배열 형태로 보내줘야 하므로, 16라인을 `password[]=aaaa`로 수정한다.

![image](https://user-images.githubusercontent.com/102066383/163726022-02eff18d-031a-48a3-9a90-7d407da435f7.png)

이 상태로 패킷을 전송하면 플래그를 획득할 수 있다.

![image](https://user-images.githubusercontent.com/102066383/163726050-c1616e11-1222-41f6-b4c2-16e7c3f3a229.png)

```
flag: DH{aede9e7fa4ccb8225f12040a16bdfd37c0c5d2f0}
```