# AWS_Server_Practice
 
### 24/01/15 ~ 

#### :video_camera: [강의 유튜브](https://www.youtube.com/playlist?list=PLHQvFs5CMVoQMcglHmtPz9ShY058H3veh)    &    :page_facing_up: [강의 참고 블로그](https://cholol.tistory.com/482)

---

## 서버 개발자가 하는 일
1. API(= TR or RPC) 만들기
2. 배치 만들기
3. DB 테이블 만들기

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

**micro service architecture(MSA) = 각각의 기능별로 서버를 쪼개는 개념** <br/>
**docker가 등장 &rightarrow; 컨테이너로 서버를 운영/배포/관리가 쉬워짐** <br/>
***해당 실습에서는 Django와 nginx를 각각의 Docker로 여는 것이 목표!!*** <br/>

* Docker 설치
  - `curl -fsSL https://get.docker.com/ | sudo sh` (docker 설치)
    
  - `sudo usermod -aG docker $USER` (현재 접속중인 사용자에게 권한 주기)
    
  - `mkdir docker-server` (docker의 이미지들을 관리할 디렉토리 생성)

* Django docker container 구성
  - 해당 github를 클론하여 django 불러오기
    
  - `vi Dockerfile`로 docker 사전 설정 작성 (docker 실행 시 사전 설정 파일이 실행됨)
    + ![image](https://github.com/NamSangwon/AWS_Server_Practice/assets/127469500/26beb411-6140-4e5c-94c0-37aacbb18c0a)
      
  - `docker build -t aws_server_prac/django .` (django의 docker 빌드하기 **경로명은 반드시 소문자로!!**)
    + `apt-get update`에서의 **에러** 발생 &rightarrow; `RUN echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list`의 명령어를 추가하여 해결 [[참고](https://www.sysnet.pe.kr/2/0/13331)]
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
    + nginx.conf & nginx-app.conf & Dockerfile 추가 [[참고](https://cholol.tistory.com/489)]
      - ***`./nginx/nginx-app.conf`의 upstream uwsgi 내의 server를 unix:/srv/docker-server/django.sock
 &rightarrow; unix:/srv/docker-server/django.sock 변경 必 (./AWS_Server_Prac/django.sock과 ./nginx/nginx-app.conf 내의 server의 .sock를 일치시켜야 함)***
    + `docker build -t docker-server/nginx .` (docker 빌드하기)
    + `docker run -p 80:80 docker-server/nginx` (nginx docker 실행하기)
 
* docker-compose 구성
  - 여러 개의 docker 이미지를 한 번에 관리하는 툴인 docker-compose 설치
    + ```
      sudo curl -L https://github.com/docker/compose/releases/download/1.25.0-rc2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
      ```
    + `sudo chmod +x /usr/local/bin/docker-compose` (실행 권한 주기)

  - 환경 관리 파일 docker-compose.yml 작성
    + ***`depends_on`이 유의해야할 점 (DB &rightarrow; django &rightarrow; nginx 순으로 실행하는 것이 오류를 발생시키지 않아 안전하기 때문)***
    +  ![image](https://github.com/NamSangwon/AWS_Server_Practice/assets/127469500/8ee9d92e-7987-4514-938e-7efe764c4d68)

  - `docker-compose up -d --build` (up == docker-compose를 실행 &rightarrow; 실행 시 빌드하여 django & nginx의 docker image 생성 및 실행)
    
  - 실행 == `docker-compose up` & 종료 == `docker-compose down`
    + django의 소스 파일만을 업데이트 시 `./AWS_Server_Prac/` 내에서 git을 pull하고 docker-compose를 재실행 해주면 됨

---

### 4. API 구성 1

* Docker에 MySQL 띄우기
  - `docker-server` 디렉토리와 같은 위치에 `mkdir mysql` (*docker-server내에 DB를 생성하면 docker 종료 시 DB가 모두 날라가기 때문*)
    
  - `docker-server` 디렉토리와 같은 위치에 `mkdir scripts` (쉘 및 배치 프로그램 저장할 용도로 생성)
    + `scripts` 디렉토리 내에 `mysql-docker.sh` 생성 (mysql 실행 스크립트 파일)
    + ![image](https://github.com/NamSangwon/AWS_Server_Practice/assets/127469500/c2486c12-ed77-4b48-87a2-81b1d49e1554)
    + `chmod +x mysql-docker.sh`로 스크립트 파일을 실행 파일로 변경 &rightarrow; `./mysql-docker.sh`로 바로 실행 가능

  - *AWS 서버 내에서 DB를 사용하기 위해 **3306 포트** 권한 설정*
 
  - Django 프로젝트의 사용 DB 변경
    + Django 프로젝트의 setting.py 내의 설정 변경 (DATABASE & INSTALLED_APPS)
      - INSTALLED_APPS에 rest_framework 추가
      - DATABASE를 sqlite에서 mysql로 설정 변경
      ```python
      # Database (in setting.py)
      DATABASES = {
          'default': {
             'ENGINE': 'django.db.backends.mysql',
             'HOST': '43.201.60.58',
             'NAME': 'AWS_Server_Prac',
             'USER': 'root',
             'PASSWORD': 'admin123!',
             'PORT': '3306',
             'OPTIONS': {'charset': 'utf8mb4'},
         }
      }
      ```
    + `pip install mysqlclient` (setting.py를 위와 같이 변경시키기 위해 필요한 모듈 설치)
    + `python manage.py makemigrations` & `python manage.py migration` (migrate 진행 &rightarrow; django에서 기본으로 제공하는 테이블 생성)
      - MYSQL과 Django 간의 버전 오류 발생 &rightarrow; ***Django의 버전을 3.2.23으로 다운그레이드로 해결*** [[참고](https://stackoverflow.com/questions/75986754/django-db-utils-notsupportederror-mysql-8-or-later-is-required-found-5-7-33)]
 
  - ***로컬에서 Django를 띄워도 setting.py 내의 DATABASE 설정에 의해 AWS EC2 내의 MySQL DB를 보게 됨***

* Django & DRF(Django Restful-Framework)를 통한 API 구현
  - **`pip install djangorestframework` (DRF 설치)**
 
  - `python manage.py startapp login` (로그인 앱 생성) [[영상](https://www.youtube.com/watch?v=NCRFC5lo8WA&list=PLHQvFs5CMVoQMcglHmtPz9ShY058H3veh&index=10) 및 [블로그](https://cholol.tistory.com/497) 구현 참고!]
    + ***setting.py의 INSTALLED_APPS에 해당 앱 추가 필요***
    + models.py 구성 (DB 테이블 구성) &rightarrow; `python manage.py makemigrations` & `python manage.py migrate`를 통해 DB 업데이트 (LoginUser 테이블 추가)
    + views.py (api call 구성)
    + urls.py (url 구성) (**AWS_Server_Prac/urls.py와 include를 통해 연결 必**)

---

### 4. API 구성 2

* Serialization (직렬화)
  - 다수의 데이터를 입력 받을 시 `user_id = request.data.get('user_id')`와 같은 코드를 통해 입력 받기 힘들기 때문에 Serialization을 사용하여 해결
 
  - 입력 받은 데이터(ex. 코드 내의 객체, 해시, 딕셔너리 등)를 JSON의 데이터를 자동으로 변환
    + `serialize.py` 파일 생성 후 *데이터 직렬화 시키는 코드* 작성
    + `serializer = LoginUserSerializer(request.data)`를 통해 serializer를 사용하여 `views.py`에 적용
    + ***[자세한 실습 사항은 github에 commit된 내용 및 강의 블로그와 영상을 참고!!]***
    + 역직렬화 : 반대로 Json 데이터를 객체, 해시, 딕셔너리 등으로 변환

---

### 5. Todo-List 앱 구성 

**Django 구성을 위주로 진행할 예정이기 때문에 *강의 블로그 및 영상* 참고!!** <br/>
***Todo-List의 프론트엔드는 [해당 github 링크](https://github.com/tkdlek11112/todo-list)을 docker에 띄워서 실습을 진행!! (3000번 포트에서 3001번 포트로 docker에 전송)***

1. Login & Regist 구현
2. Todo Task (Create & Select & Delete & Toggle) 구현
3. 페이징 처리
4. 공통 영역 추가 (함수와 비슷하게 공통 패키지에 구현하여 재사용성을 높이도록 하는 방법)
   - body 부로 넘기던 *user_id*를 *version*와 함께 headers로 넘기도록 수정 (공통 영역 TodoView 내에서 입력 받기)
   - `Access to XMLHttpRequest at 'http://localhost:8000/todo/select' from origin 'http://localhost:3001' has been blocked by CORS policy: Request header field version is not allowed by Access-Control-Allow-Headers in preflight response.` 에러 발생 &rightarrow; `setting.py`를 수정하여 오류 해결 [[수정 사항](https://github.com/NamSangwon/AWS_Server_Practice/commit/eb7a6a4a1a27bbeb42648b954ad1cac4634016af)]
   - 각 API의 출력을 공통 포맷으로 수정

---

### 6. Django Log 찍기

***로컬 환경에서만 프로그래밍을 진행할 수 없기 때문에 Log를 확인하는 것이 중요함*** <br>

* Django에서 제공하는 Logging 사용하기
  - `import logging`을 통해 사용
  - `logger = logging.getLogger('django')`를 통해 로그를 찍기 위한 변수 생성
  - `debug()`, `info()`, `warning()`, `error()`, `critical()`와 같은 함수들을 통해 로그를 찍음 (용도에 따라 다음 함수 중 하나를 사용 [ex. `error()`는 에러가 발생했을 시 사용])

* 로그 포맷
  - 로그 찍히는 포맷을 setting.py의 LOGGING에 아래와 같은 코드를 추가하여 정의 가능
  - ```
    'formatters': { # 로그 포맷 구성
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    }
    ```
  - handlers의 file내에 `'formatter':'verbose'`를 추가하여 정의한 포맷을 적용 (아래는 포맷이 적용된 로그 결과)
  - ```
    C:\Users\nsw32\vscode\AWS_Server_Practice\AWS_Server_Prac\settings.py changed, reloading.
    INFO 2024-01-25 18:51:02,790 autoreload 14788 376 Watching for file changes with StatReloader
    INFO 2024-01-25 18:51:05,891 views 14788 18292 Test API Start!!
    INFO 2024-01-25 18:51:05,891 views 14788 18292 input_value1 = 1
    INFO 2024-01-25 18:51:05,891 views 14788 18292 input_value2 = 2
    INFO 2024-01-25 18:51:05,891 views 14788 18292 input_value3 = 3
    INFO 2024-01-25 18:51:05,891 views 14788 18292 output_value1 = 12
    INFO 2024-01-25 18:51:05,891 views 14788 18292 output_value2 = 23
    INFO 2024-01-25 18:51:05,892 views 14788 18292 output_value3 = 31
    INFO 2024-01-25 18:51:05,892 views 14788 18292 Test API End!!
    ERROR 2024-01-25 18:51:05,892 views 14788 18292 Occured Error, user_id = asd
    WARNING 2024-01-25 18:51:05,892 views 14788 18292 [Warning!!] user_id = asd
    INFO 2024-01-25 18:51:05,892 basehttp 14788 18292 "POST /todo/test HTTP/1.1" 200 112
    ```

--- 

### 7. 배치 프로그램

* ***배치(batch) 프로그램 = 일괄적으로 처리하는 프로그램***

* 배치라는걸 만드는 것보다 배치를 **언제 써야하는가**가 중요함

* *알고리즘을 적용하여 배치 프로그램을 최적화*

* Django에서 제공하는 배치 프로그램 생성
  - 해당 프로젝트에서는 `./common/management/commands/(command 파일명)` 파일에 배치 프로그램 생성
  - `python manage.py (배치 파일명)`으로 배치 프로그램 실행 (*동일한 명령어로 작동하는 makemigrations, migrate와 runserver도 모두 commands이다.*)
  - ```
    # 실습 배치 프로그램
    from django.core.management.base import BaseCommand # Django에서 제공하는 Command 클래스
    from todo.models import Task
    from datetime import datetime
    
    # 오늘 날짜 이전에 생성한 Task들의 state를 update
    class Command(BaseCommand):
        def handle(self, *args, **options):
            task_list = Task.objects.all()
    
            for task in task_list:
                if task.end_date < datetime.now().date():
                    task.state = 3
                    task.save()
                    print(task.id, task.name, "만료되었습니다.", task.end_date)
    ```
    - 배치 프로그램은 보통 *특정 시간* 혹은 *특정 조건*에 작동 &rightarrow; 스케쥴러 역할로 제공하는 크론탭(in Linux) or Jenkins 사용
      * Jenkins는 배치 프로그램의 종료를 특정 조건으로 사용할 수 있기 때문에 더 유용하게 사용 가능

---

# 8. Amazon Aurora DB

* AWS의 RDS를 통해 DB 생성 (상세한 설명은 [강의 블로그](https://cholol.tistory.com/538) 및 [강의 영상](https://www.youtube.com/watch?v=tJMSjUvDGss&list=PLHQvFs5CMVoQMcglHmtPz9ShY058H3veh&index=2) 참고)

* Django와 AWS에서 생성한 DB 연결
  - `mysqlclient` 사용 (아래는 MySQL DB 설정 코드)
  - ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST':  'database-1.cluster-cahfm1ikomik.ap-northeast-2.rds.amazonaws.com', # os.environ['MYSQL_HOST'] (환경 변수 사용) # AWS DB의 Writer Instance의 Endpoint name
            'NAME': 'djangodb', # AWS DB 생성 시 설정한 데이터베이스 name
            'USER': 'mychew', # os.environ['MYSQL_USER'] (환경 변수 사용)
            'PASSWORD': 'cholol.tistory.com', # os.environ['MYSQL_PASSWORD'] (환경 변수 사용)
            'PORT': '3306',
            'OPTIONS': {'charset': 'utf8mb4'},
        }
    }
    ```
  - 위와 같이 USER와 PASSWORD를 설정으로 작성할 시
    + 누군가 확인할 수 있는 위험 有 &rightarrow; **환경변수로 계정 정보 관리** (예로 위의 주석과 같이 작성)
    
* DB Tool을 통해 AWS DB 읽기
  - 위의 MySQL DB 설정 코드와 똑같이 설정하여 DB Tool에 생성
  - `javax.net.ssl.SSLHandshakeException: No appropriate protocol ...`과 같은 오류가 발생 시 `Enable TLSv1`을 클릭하여 해결
  - 위를 완료하면 `python manage.py migrate`를 통해 Django에서 migrate AWS DB에 Django에서 제공하는 기본 테이블 생성
 
* Parameter Group을 통해 Parameter를 설정하여 사용 가능

---

### 9. Swagger를 통해 API 문서화

* `pip install drf-yasg`를 통해 Django에서 Swagger를 사용하기 위한 drf-yasg 라이브러리 설치
  - `INSTALLED_APPS`에 'drf_yasg' 추가
  - `./AWS_Server_Prac/urls.py`에 아래 코드 추가
  - ```
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    from rest_framework import permissions
    
    schema_view = get_schema_view(
        openapi.Info(
            title="TO-DO API",  # 타이틀
            default_version='v1',   # 버전
            description="서버개발자가 되는법 #12",   # 설명
            terms_of_service="https://cholol.tistory.com/551",
            contact=openapi.Contact(email="mychew@kakao.com")
    ),
        validators=['flex'],
        public=True,
        permission_classes=(permissions.AllowAny,)
    )

    urlpatterns = [
        # swagger
        path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
        # django
        ...
    ]
    ```
  - ![image](https://github.com/NamSangwon/AWS_Server_Practice/assets/127469500/5784551e-ce86-4274-8e26-f8ab9e09a17b)

* swagger에 API 정보를 노출시키기
  - `from drf_yasg.utils import swagger_auto_schema`
  -  [INPUT INFO] `@swagger_auto_schema((parameters...))`를 통해 swagger에 API 정보를 노출시키기 위해 annotation(@) 추가 해주기
    + ```
      @swagger_auto_schema(tags=['Todo 만들기'], 
                           request_body=TodoSerializer, 
                           query_serializer=TodoSerializer,
                           responses={
                               200 : '성공',
                               404 : '찾을 수 없음',
                               400 : '인풋 값 에러',
                               500 : '서버 에러'
                           })
      ``` 
    + ![image](https://github.com/NamSangwon/AWS_Server_Practice/assets/127469500/d24d0e1b-dc70-4844-b9b8-4283fae1e061)
  - [OUTPUT INFO] openapi.schema()를 통해 status=200 일 때의 OUTPUT 값 정보 출력
    + ```
      from drf_yasg import openapi
      
      id_field = openapi.Schema(
           'id',
           description='To-Do가 생성되면 자동으로 채번되는 ID값',
           type=openapi.TYPE_INTEGER
       )
   
       success_response = openapi.Schema(
           title='response',
           type=openapi.TYPE_OBJECT,
           properties={
               'id': id_field
           }
       )

      @swagger_auto_schema(...,
                           responses={
                               200 : success_response,
                               ...
                           })
      ```
    + ![image](https://github.com/NamSangwon/AWS_Server_Practice/assets/127469500/c3149fdb-3034-41a9-a0a1-60c6decc2435)
   
  - 주석으로 마크다운 형태로 swagger에 반영됨
    + ![image](https://github.com/NamSangwon/AWS_Server_Practice/assets/127469500/1a04b154-c883-472d-bf0b-240c75f5637d)
