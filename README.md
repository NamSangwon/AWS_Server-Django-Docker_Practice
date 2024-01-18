# AWS_Server_Practice
 
### 24/01/15 ~ 

#### [강의 유튜브](https://www.youtube.com/playlist?list=PLHQvFs5CMVoQMcglHmtPz9ShY058H3veh) & [강의 참고 블로그](https://cholol.tistory.com/482)

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
---
### 2. 개발 환경 구성 2
![image](https://github.com/NamSangwon/AWS_Server_Practice/assets/127469500/94441b73-7c72-4e21-b219-10baa3d8bb2d)

[pip를 이용하기 위해 가상 환경에서 진행 (`source venv/bin/activate`)]

* uwsgi
  - wsgi(Web Server Gateway Interface) == 웹서버와 웹 프레임워크 사이에 통신을 담당하는 인터페이스
  - `pip install uwsgi` (uwsgi 설치)
  - `uwsgi --http :8000 --module server_dev.wsgi` -> 서버에서 Django 실행
    + -- http :8000 == 0.0.0.0:8000
    + --module server_dev.wsgi == Django를 wsgi로 실행
  - 
  
* Nginx
  -
  
* MySQL
  -
