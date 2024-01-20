from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LoginUser
from django.contrib.auth.hashers import make_password, check_password # 장고에서 제공하는 암호화

# Create your views here.

class AppLogin(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        user_pw = request.data.get('user_pw')
        
        user = LoginUser.objects.filter(user_id=user_id).first()

        if user is None:
            return Response(dict(msg="해당 사용자가 없습니다."))
        
        if check_password(user_pw, user.user_pw): # 입력받은 pw와 DB 내의 pw 비교
            return Response(dict(msg="로그인 성공!"))
        else:
            return Response(dict(msg="로그인 실패, 비밀번호 틀림!"))

class RegistUser(APIView): 
    def post(self, request):
        user_id = request.data.get('user_id')
        user_pw = request.data.get('user_pw')
        user_pw_encrypted = make_password(user_pw) # 암호화


        # 중복 아이디 예외 처리 (추가적으로 아이디가 한글, 특수문자 등이 추가되는 지와 같은 다양한 예외 추가 必)
        user = LoginUser.objects.filter(user_id=user_id).first()
        if user is not None: 
            return Response(dict(msg="동일한 아이디가 존재합니다."))
        else:
            LoginUser.objects.create(user_id=user_id, user_pw=user_pw_encrypted) # DB에 입력 받은 데이터 추가

        data = dict(
            user_id = user_id,
            user_pw = user_pw_encrypted
        )
        
        return Response(data)
