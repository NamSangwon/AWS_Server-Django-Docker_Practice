from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LoginUser
from django.contrib.auth.hashers import make_password, check_password # 장고에서 제공하는 암호화
from .serialize import LoginUserSerializer

# Create your views here.

################################## 실습 코드 ##################################
class RegistUser(APIView):
    def post(self, request):
        user_id = request.data['user_id']
        user_pw = request.data['user_pw']

        # 공백 입력 예외 처리
        if user_id == '' or user_pw == '' or user_id is None or user_pw is None:
            return Response(data=dict(msg="아이디나 비밀번호는 공백이 될 수 없습니다."))
        
        # 비밀번호 암호화 처리
        user_pw_encrypted = make_password(user_pw)

        # 중복 아이디 예외 처리
        if LoginUser.objects.filter(user_id=user_id).exists():
            return Response(data=dict(msg="이미 존재하는 아이디입니다."))

        LoginUser.objects.create(user_id=user_id, user_pw=user_pw_encrypted)

        return Response(data=dict(msg="회원가입에 성공했습니다.", user_id=user_id))
    
class AppLogin(APIView):
    def post(self, request):
        user_id = request.data['user_id']
        user_pw = request.data['user_pw']
        user = LoginUser.objects.filter(user_id=user_id).first()

        # 존재하지 않는 ID 예외 처리
        if user is None:
            return Response(dict(msg="해당 사용자가 없습니다."))
        
        # 입력받은 pw와 DB 내의 pw 비교
        if check_password(user_pw, user.user_pw): 
            # 로그인 성공 시 아이디 반환
            return Response(dict(
                msg="로그인 성공!",
                user_id = user.user_id
            ))
        # 비밀번호 틀릴 시 예외 처리
        else:
            return Response(dict(msg="로그인 실패, 비밀번호 틀림!"))

# 서버에서 로그인과 로그아웃 로그를 확인할 필요가 생길 떄도 있기 때문에 구현
class AppLogOut(APIView):
    def post(self, request):
        # 로그아웃한 시간
        return Response(status=200)
    
###############################################################################

################################## 샘플 코드 ##################################
# class AppLogin(APIView):
#     def post(self, request):
#         user_id = request.data.get('user_id')
#         user_pw = request.data.get('user_pw')
        
#         user = LoginUser.objects.filter(user_id=user_id).first()

#         if user is None:
#             return Response(dict(msg="해당 사용자가 없습니다."))
        
#         if check_password(user_pw, user.user_pw): # 입력받은 pw와 DB 내의 pw 비교
#             # 로그인 성공 시 개인 정보 반환
#             return Response(dict(
#                 msg="로그인 성공!",
#                 user_id = user.user_id,
#                 birth_day = user.birth_day, 
#                 gender = user.gender, 
#                 email = user.email, 
#                 name = user.name, 
#                 age = user.age
#             ))
#         else:
#             return Response(dict(msg="로그인 실패, 비밀번호 틀림!"))

# class RegistUser(APIView): 
#     def post(self, request):
#         # user_id = request.data.get('user_id')
#         # user_pw = request.data.get('user_pw')

#         # # 개인 정보 
#         # birth_day = request.data.get('birth_day', None)
#         # gender = request.data.get('gender', "male")
#         # email = request.data.get('email', "")
#         # name = request.data.get('name', "")
#         # age = request.data.get('age', 20)

#         # user_pw_encrypted = make_password(user_pw) # 암호화

#         serializer = LoginUserSerializer(request.data)

#         # 중복 아이디 예외 처리 (추가적으로 아이디가 한글, 특수문자 등이 추가되는 지와 같은 다양한 예외 추가 必)
#         if LoginUser.objects.filter(user_id=serializer.data['user_id']).exists():
#             dup_user = LoginUser.objects.filter(user_id=serializer.data['user_id']).first()
#             data = dict(
#                 msg="동일한 아이디가 존재합니다.",
#                 user_id = dup_user.user_id,
#                 user_pw = dup_user.user_pw
#             )
#             return Response(data)
        
#         # 데이터 직렬화 (create() 내에서 비밀번호 암호화 처리 完) (LoginUser.objects.create(**validated_data)로 만들어진 Django 모델)
#         user = serializer.create(request.data)
        
#         return Response(data=LoginUserSerializer(user).data) # Django 모델을 직렬화한 데이터(JSON) 반환
