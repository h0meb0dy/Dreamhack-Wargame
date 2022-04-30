# [DreamHack] broken-png

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 드림컴퍼니에서 디자이너로 일하는 드림이는 직장 동료에게 내일 사용해야 하는 드림뱅크의 홍보 이미지를 메일을 통해 전달 받았습니다. 하지만 이메일 전송 과정에서 문제가 발생해 이미지가 정상적으로 전달되지 않았습니다.
>
> > 드림이: 전달해주신 홍보 이미지가 원래 정사각형으로 알고 있는데, 반밖에 오지 않은 것 같아요! 다시 보내 주실 수 있나요?
> > 드림뱅크 직원: 담당 직원이 어제 퇴사를 해서 지금 당장 이미지를 다시 전달 드리기 어렵습니다.
> > 드림이: 네?
>
> 드림이를 위해 오늘 오후 6시까지 깨진 이미지를 복구해주세요!
>
> Release: [broken-png.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8597580/broken-png.zip)

## Analysis

![image](https://user-images.githubusercontent.com/104156058/166117751-a97b59ad-0358-4063-bcf1-bb62ed776004.png)

사진을 열어보면 `DH{`까지만 보이고 나머지는 잘려있다. 문제 설명에서 이미지가 반밖에 오지 않았다고 했으니, 아래 절반을 복구해야 하는 것 같다.

## Solve

PNG 파일의 이미지 크기 정보는 IHDR 청크에 저장되어 있다.

![image](https://user-images.githubusercontent.com/104156058/166117811-66f5f115-9280-4baf-9762-a566110e6ef6.png)

문제에서 제공된 이미지를 HxD로 열어서 IHDR 청크 부분을 보면,

![image](https://user-images.githubusercontent.com/104156058/166117862-e7475d2a-9f84-4829-a88e-3eef3ad87364.png)

`IHDR` 바로 다음의 4바이트인 `00 00 02 00`이 width를 의미하고, 바로 다음의 `00 00 01 00`이 height를 의미한다. height가 width의 절반으로 설정되어 있어서 이미지가 잘려 보이는 것이다. height를 `00 00 02 00`으로 바꾸고 이미지를 열어보면 플래그를 획득할 수 있다.

![image](https://user-images.githubusercontent.com/104156058/166117924-66c84f7e-a68a-4c91-b8ac-d89fe779c162.png)

![image](https://user-images.githubusercontent.com/104156058/166117934-f8cdf002-188f-4241-b87d-e3428aa1706b.png)

```
flag: DH{image_height_property}
```