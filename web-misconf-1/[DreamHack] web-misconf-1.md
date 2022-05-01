# [DreamHack] web-misconf-1

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 기본 설정을 사용한 서비스입니다.
> 로그인한 후 Organization에 플래그를 설정해 놓았습니다.
>
> Release: [web-misconf-1.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8598168/web-misconf-1.zip)

`defaults.ini`에서 관리자 계정과 비밀번호를 알아낼 수 있다.

```ini
#################################### Security ############################
[security]
# disable creation of admin user on first start of grafana
disable_initial_admin_creation = false

# default admin user, created on startup
admin_user = admin

# default admin password, can be changed before first start of grafana, or in profile settings
admin_password = admin
```

admin/admin으로 로그인을 하면 대시보드가 뜨는데,

![image](https://user-images.githubusercontent.com/104156058/166129827-3992f8a9-14ef-4234-9c31-48f3605f9fee.png)

Server Admin - Settings로 들어가면 `defaults.ini`에 있는 항목들을 확인할 수 있다. org_name을 찾으면 플래그를 획득할 수 있다.

![image](https://user-images.githubusercontent.com/104156058/166129846-692a368e-b48d-4f33-a198-e35410355680.png)

```
flag: DH{default_account_is very dangerous}
```