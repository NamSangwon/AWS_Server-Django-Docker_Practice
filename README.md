# AWS_Server_Practice
 
### 24/01/15 ~ 

#### :video_camera: [강의 유튜브](https://www.youtube.com/playlist?list=PLHQvFs5CMVoQMcglHmtPz9ShY058H3veh)    &    :page_facing_up: [강의 참고 블로그](https://cholol.tistory.com/482)

---

### 1. 개발 환경 구성 1
* AWS 서버 생성
  - 플랫폼 : Linux
  - SSH 프로토콜 사용
  - 보안 규칙
    + 서버 접속 : 22번 포트 사용
    + 서버에서 띄운 Django에 접속 : 8000번 포트 사용

* PuTTY를 통한 SSH 서버 연결
  - 서버 IP 주소 & 서버 구성 시 생성한 키를 기반으로 연결

* 서버(Ubuntu) 환경 구성
  - 로컬 환경에서 Django 설치 및 구성 후 github에 commit & push
  - 서버에서 github에 등록된 파일 pull하여 구성
  - `sudo apt update` (설치 가능한 패키지 리스트를 최신화)
  - `sudo apt install python3` (파이썬 설치)
  - `sudo apt install python3-pip` (pip 설치)
  - `pip3 install virtualenv` & `sudo apt install virtualenv` (가상 환경 virtualenv 설치)
  - `virtualenv venv --python=python3` (python3 버전으로 가상 환경 venv 구성)
  - `source venv/bin/activate` (가상 환경 실행)
  - 필요 모듈 추가 
    + [로컬 환경] `pip freeze > requirements.txt` (로컬 환경에서 사용된 모듈들을 txt 파일로 내보내기)
    + github에 commit & push
    + [서버 환경] pull -> `pip install -r requirements.txt` (필요 모듈을 서버 환경에 추가)
    + 
---

### 2. 개발 환경 구성 2
![image](https://github.com/NamSangwon/AWS_Server_Practice/assets/127469500/94441b73-7c72-4e21-b219-10baa3d8bb2d)

#### [pip를 이용하기 위해 가상 환경에서 진행 (`source venv/bin/activate`)]
#### `ps -ef | grep (프로그램명)` &rightarrow; 설정 적용 확인

* uwsgi (+ socket)
  - wsgi(Web Server Gateway Interface) == 웹서버와 웹 프레임워크 사이에 통신을 담당하는 인터페이스
    
  - `pip install uwsgi` (uwsgi 설치)
    
  - `uwsgi --http :8000 --module server_dev.wsgi` -> 서버에서 Django 실행
    + -- http :8000 == 0.0.0.0:8000
    + --module server_dev.wsgi == Django를 wsgi로 실행
      
  - uwsgi 커스텀 설정
    + etc 디렉토리에 uwsgi/sites/ 디렉토리 생성
    + `sudo vi AWS_Server_Prac` (/etc/uwsgi/sites/에 파일 작성) 
    + ![image](https://github.com/NamSangwon/AWS_Server_Practice/assets/127469500/8f60c94d-1411-4728-a661-3d3b252a0094)
    + `sudo mv AWS_Server_Practice AWS_Server_Practice.ini` (.ini로 파일명 변경)
      
  - `uwsgi -i /etc/uwsgi/sites/AWS_Server_Prac.ini` (uwsgi 커스텀 설정 적용)
    + `AWS_Server_Prac.ini` 파일은 **# 주석 처리 불가**이므로 **유의!**
    + `uwsgi -i /etc/uwsgi/sites/AWS_Server_Prac.ini -http :8000`으로 **config파일을 이용해서 uwsgi를 실행**
    + ***/tmp/ 디렉토리에서 `tail -f uwsgi.log`을 통해 로그 찍기***
  
* Nginx
  - `sudo apt-get install nginx` (nginx 설치) &rightarrow; 설치 시 기본 디렉토리 생성됨
    
  - `/etc/nginx/nginx/nginx.conf` &rightarrow; ***[nginx의 config](https://cholol.tistory.com/485)는 서버 개발 역량에 필수이므로 확인 요망!!***
    
  - `/etc/nginx/sites-enabled/default` 에서 실질적인 설정을 조정함 &rightarrow; 포트 번호를 80에서 8080으로 변경함
    
  - nginx의 virtual host config로 config파일 생성
    
  - ![image](https://github.com/NamSangwon/AWS_Server_Practice/assets/127469500/eadd8972-b0ca-49b5-a3a8-dfa180fd4e74)
    
  - ### nginx 가동 &rightarrow; /etc/nginx/nginx.conf에서 /etc/nginx/sites-enables/AWS_Server_Practice를 읽어서 80(http) 포트번호로 들어오는 요청을 uwsgi로 전송
    
  - ***`sudo systemctl start nginx`으로 nginx 실행***
    + AWS 인스턴스에 인바운드 규칙(HTTP, HTTPS, etc.) 추가

---

### 3. Docker로 서버 띄우기

**micro service architecture(MSA) = 각각의 기능별로 서버를 쪼개는 개념**
**docker가 등장 &rightarrow; 컨테이너로 서버를 운영/배포/관리가 쉬워짐**
***해당 실습에서는 Django와 nginx를 각각의 Docker로 여는 것이 목표!!***

* Docker 설치
  - `curl -fsSL https://get.docker.com/ | sudo sh` (docker 설치)
    
  - `sudo usermod -aG docker $USER` (현재 접속중인 사용자에게 권한 주기)
    
  - `mkdir docker-server` (docker의 이미지들을 관리할 디렉토리 생성)

* Django docker container 구성
  - 해당 github를 클론하여 django 불러오기
    
  - `vi Dockerfile`로 docker 사전 설정 작성 (docker 실행 시 사전 설정 파일이 실행됨)
    + ![image](https://github.com/NamSangwon/AWS_Server_Practice/assets/127469500/26beb411-6140-4e5c-94c0-37aacbb18c0a)
      
  - `docker build -t aws_server_prac/django .` (django의 docker 빌드하기 **경로명은 반드시 소문자로!!**)
    + `apt-get update`에서의 **에러** 발생 &rightarrow; `RUN echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list`의 명령어를 추가하여 해결 ([참고](https://www.sysnet.pe.kr/2/0/13331))
    + `RUN pip install -r requirements.txt`에서의 **에러** 발생 &rightarrow; requirements.txt 내의 django와 asgief의 버전을 다운그레이드하여 해결
    + `docker image ls` (docker 이미지 확인)
      
  - `docker run -p 8000:8000 aws_server_prac/django` (docker 실행 &rightarrow; 사전 설정 파일에 작성된 CMD를 통해 바로 django 서버 실행)
    + `docker run -d -p 8000:8000 aws_server_prac/django` (***-d == 데모 실행 (백그라운드 실행)*** &rightarrow; `docker ps`를 통해 실행 유무 확인)
    + `-p 8000:8000`은 ubuntu 서버와 docker 서버 간의 연결을 의미

* Nginx docker container 구성
  - *nginx와 django의 연결을 위한 uwsgi를 requirements.txt에 추가하여 설치*
    
  - *`/docker-server/AWS_Server_Prac/Dockerfile`의 EXPOSE & CMD 불필요하므로 주석 처리*
    
  - *`/docker-server/AWS_Server_Prac/uwsgi.ini` 추가*
    + ![image](https://github.com/NamSangwon/AWS_Server_Practice/assets/127469500/419b1216-62f7-4949-8ecb-784b8b9ac1e4)
   
  - **nginx 설정** 
    + nginx.conf & nginx-app.conf & Dockerfile 추가 ([참고](https://cholol.tistory.com/489))
    + `docker build -t docker-server/nginx .` (docker 빌드하기)
    + `docker run -p 80:80 docker-server/nginx` (nginx docker 실행하기)
 
* docker-compose 구성
  - 여러 개의 docker 이미지를 한 번에 관리하는 툴인 docker-compose 설치
    + `sudo curl -L https://github.com/docker/compose/releases/download/1.25.0-rc2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose`
    + `sudo chmod +x /usr/local/bin/docker-compose` (실행 권한 주기)

  - 환경 관리 파일 docker-compose.yml 작성
    + ***`depends_on`이 유의해야할 점 (DB &rightarrow; django &rightarrow; nginx 순으로 실행하는 것이 오류를 발생시키지 않아 안전하기 때문)***
    +  ![image](https://github.com/NamSangwon/AWS_Server_Practice/assets/127469500/8ee9d92e-7987-4514-938e-7efe764c4d68)

  - `docker-compose up -d --build` (up == docker-compose를 실행 &rightarrow; 실행 시 빌드하여 django & nginx의 docker image 생성 및 실행)

  -  ***`./nginx/nginx-app.conf`의 upstream uwsgi 내의 server를 unix:/srv/docker-server/django.sock
 &rightarrow; unix:/srv/docker-server/django.sock 변경 必 (./AWS_Server_Prac/django.sock과 ./nginx/nginx-app.conf 내의 server의 .sock를 일치시켜야 함)***
