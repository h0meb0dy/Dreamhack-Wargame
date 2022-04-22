# [DreamHack] Carve Party

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 할로윈 파티를 기념하기 위해 호박을 준비했습니다! 호박을 10000번 클릭하고 플래그를 획득하세요!
>
> Release: [Carve Party.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8539802/Carve.Party.zip)

## Analysis

![image](https://user-images.githubusercontent.com/102066383/163727607-b952e0c6-40a9-4048-8297-f2e1caadef4b.png)

호박을 클릭하면 맨 아래의 숫자가 1씩 줄어들고, 0 more clicks to go가 되면 플래그를 얻을 수 있을 것 같다.

```javascript
$(function() {
  $('#jack-target').click(function () {
    counter += 1;
    if (counter <= 10000 && counter % 100 == 0) {
      for (var i = 0; i < pumpkin.length; i++) {
        pumpkin[i] ^= pie;
        pie = ((pie ^ 0xff) + (i * 10)) & 0xff;
      }
    }
    make();
  });
});
```

소스 코드의 맨 아래쪽에 호박을 클릭했을 때의 동작이 함수로 정의되어 있다. 이 함수를 개발자 도구의 콘솔에서 호출하면 마우스로 클릭한 것과 같은 효과가 있다.

![image](https://user-images.githubusercontent.com/102066383/163727644-048351eb-4995-4f59-ad2f-67997a1b301d.png)

이 함수를 10000번 반복해서 호출하면 플래그를 획득할 수 있다.

![image](https://user-images.githubusercontent.com/102066383/163727702-d88644cf-10f6-46ed-b241-049803037b4d.png)

> 10000번 하면 0 more clicks to go가 되는데, 이 상태에서 한 번 더 클릭을 해야 플래그를 준다.

```
flag: DH{I_lik3_pumpk1n_pi3}
```