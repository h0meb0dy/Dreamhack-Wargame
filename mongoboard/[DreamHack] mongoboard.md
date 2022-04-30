# [DreamHack] mongoboard

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> node와 mongodb로 구성된 게시판입니다.
> 비밀 게시글을 읽어 FLAG를 획득하세요.
>
> - MongoDB < 4.0.0
>
> Release: [mongoboard.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8596117/mongoboard.zip)

## Analysis

![image](https://user-images.githubusercontent.com/104156058/166092628-9033e70b-167d-47c3-9087-95519782ed14.png)

서버에 접속하면 4개의 글이 있는데, admin이 작성한 FLAG라는 글만 no가 없다. 나머지 3개는 클릭하면 글의 내용을 볼 수 있는데, FLAG를 클릭하면 Secret Document!라는 메시지가 뜨면서 막힌다.

```javascript
    app.get('/api/board/:board_id', function(req, res){
        MongoBoard.findOne({_id: req.params.board_id}, function(err, board){
            if(err) return res.status(500).json({error: err});
            if(!board) return res.status(404).json({error: 'board not found'});
            res.json(board);
        })
    });
```

`index.js`를 보면, `/api/board/:board_id`로 접속할 경우 `board_id`에 해당하는 글을 찾아서, secret이든 아니든 관계없이 글의 내용을 JSON 형식으로 보내주는 것을 알 수 있다. 그러면 FLAG의 `board_id`만 알아내면 될 것이다.

![image](https://user-images.githubusercontent.com/104156058/166092736-c66ae25e-d354-48a6-9a88-5c199a4e7ae1.png)

no를 보면 규칙성이 보이는데, 빨간 박스 이외의 부분은 모두 같다. 첫 번째 빨간 박스는 3, 6, ..., b로 커지는 규칙성이 있으므로 7부터 a 중 하나라고 추측할 수 있고, 두 번째 빨간 박스는 7d, 7e, ..., 80으로 1씩 커지는 규칙성이 있으므로 7f라고 추측할 수 있다.

## Exploit

`/api/board/626cc1788612b30963fe5e7f`로 접속하니 플래그를 획득할 수 있었다.

![image](https://user-images.githubusercontent.com/104156058/166092878-8c1425ee-dce3-4ace-be14-487a2068eb91.png)

```
flag: DH{f823bac286ef352172b1cd73c812708ea356a000}
```