# [DreamHack] [wargame.kr] fly me to the moon

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> javascript game.
>
> can you clear with bypass prevent cheating system?

## Analysis

![image](https://user-images.githubusercontent.com/104156058/165702416-cb8d578a-557f-41ec-b60a-89bdaf03df76.png)

![image](https://user-images.githubusercontent.com/104156058/165702484-d593f2d6-e471-40f7-a8a3-3213b0bbbcd5.png)

우주선을 조종해서 초록색 벽을 피해야 하는 게임이다.

![image](https://user-images.githubusercontent.com/104156058/165702540-f938f075-f5e1-44c8-83f8-22b4ab6248b3.png)

죽으면 31337점을 얻어야 한다는 메시지가 뜬다.

## Exploit

죽었을 때 서버에 전달되는 패킷을 잡아보면 다음과 같다.

![image](https://user-images.githubusercontent.com/104156058/165702843-70c2c567-396c-4b48-8d6e-0a95cedc7ad7.png)

`token`과 `score`를 전송하는데, `token`은 사용자 인증을 하는 역할이고, `score`는 점수를 의미한다. `score`의 값을 31337로 바꿔서 전송하면 31337점을 얻은 것으로 처리되어 플래그를 획득할 수 있다.

![image](https://user-images.githubusercontent.com/104156058/165703105-1ec6410f-3cc8-41ad-80c3-07db2525df14.png)

```
flag: DH{8E2ACD010BECF06D784E0798E4F4E4C33E908DF5}
```