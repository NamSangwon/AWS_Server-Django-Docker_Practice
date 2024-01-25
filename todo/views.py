from rest_framework.views import APIView
from .models import Task
from rest_framework.response import Response
from datetime import datetime
from django.shortcuts import render
from common.common import TodoView, SuccessResponse, SuccessResponseWithData, CommonResponse, ErrorResponse
import logging

# Create your views here.

################################## 실습 코드 ##################################
logger = logging.getLogger('django') # 로그를 찍기 위한 변수

# 테스팅을 위한 클래스
class Test(TodoView):
    def post(self, request):
        ##########################################################
        # 디버깅을 대체하여 어디까지 코드가 진행되는지 로그 남기기
        logger.info("Test API Start!!") 

        # 인풋 
        input_value1 = request.data.get('input_value1')
        input_value2 = request.data.get('input_value2')
        input_value3 = request.data.get('input_value3')

        # 인풋 로그 찍기
        logger.info("input_value1 = " + input_value1)
        logger.info("input_value2 = " + input_value2)
        logger.info("input_value3 = " + input_value3)

        # 아웃풋 
        output_value1 = input_value1 + input_value2
        output_value2 = input_value2 + input_value3
        output_value3 = input_value3 + input_value1

        # 아웃풋 로그 찍기
        logger.info("output_value1 = " + output_value1)
        logger.info("output_value2 = " + output_value2)
        logger.info("output_value3 = " + output_value3)

        logger.info("Test API End!!")
        ##########################################################

        # ./logs/log 파일에 로그 찍기 (파일 경로는 setting.py에 작성됨)
        # level이 ERROR이므로 logger.warning()은 파일에 찍히지 않음
        logger.error("Occured Error, user_id = " + self.user_id) 
        logger.warning("[Warning!!] user_id = " + self.user_id)

        return SuccessResponseWithData(data=dict(output_value1=output_value1,
                                                output_value2=output_value2,
                                                output_value3=output_value3))

class TaskSelect(TodoView): # -> APIView를 상속하여 TaskSelect 클래스 생성
    def post(self, request):

        # 이전 버전 (body 부에 user_id를 받아 오는 버전)
        if self.user_id is False:
            user_id = request.data.get('user_id')
        # 현재 버전 (headers 부에 user_id를 받아 오는 버전)
        else: 
            user_id = self.user_id

        page_number = request.data.get('page_number')

        # Task 조회 처리
        if user_id == "" or user_id is None:
            tasks = []
        elif user_id:
            tasks = Task.objects.filter(user_id=user_id) # 해당 아이디에 해당하는 Task 조회
        else:
            tasks = Task.objects.all() # 모든 Task 조회

        # 페이징 처리 (한 페이지의 Task 수 = 10)
        is_last_page = True # 마지막 페이지 = 다음 페이지 없음
        if page_number is not None and page_number >= 0 and len(tasks) > 0:
            # 페이지 개수가 1개일 때의 마지막 페이지
            if tasks.count() <= 10:
                pass

            # 페이지 개수가 2개 이상일 떄의 마지막 페이지
            elif tasks.count() <= (1 + page_number) * 10:
                tasks = tasks[page_number * 10 : ] # 1 페이지 = 0 ~ 7 || 2 페이지 = 10 ~ 14 || ...

            # 마지막 페이지가 아닐 시
            else:
                is_last_page = False
                tasks = tasks[page_number * 10 : (1+page_number) * 10] # 1 페이지 = 0 ~ 9 || 2 페이지 = 10 ~ 19 || ...

        # 페이징 미처리
        else:
            pass

        # Task 리스트 구성
        tasks_list = []
        for task in tasks:
            tasks_list.append(dict(id = task.id,
                                name=task.name,
                                userId=task.user_id,
                                done=task.state))

        # (이전 버전도 정상적으로 작동할 수 있게 if문을 통해 version 분기))
        if self.version >= "1.1":
            return SuccessResponseWithData(dict(tasks=tasks_list, isLastPage=is_last_page))
        else:
            return Response(status=200, data=dict(tasks=tasks_list, isLastPage=is_last_page))
    
class TaskCreate(TodoView):
    def post(self, request):
        
        # 이전 버전 (body 부에 user_id를 받아 오는 버전)
        if self.user_id is None:
            user_id = request.data.get('user_id')
        # 현재 버전 (headers 부에 user_id를 받아 오는 버전)
        else: 
            user_id = self.user_id

        todo_id = request.data.get('todo_id')
        name = request.data.get('name')
        
        # Task 생성
        if todo_id:
            task = Task.objects.create(id=todo_id, user_id=user_id, name=name) # 실습 2번 (id 입력 받기)
        else:
            task = Task.objects.create(user_id=user_id, name=name) # 실습 3번 (id 입력 받지 않기)

        # 사용자 편의를 위해 프론트엔드는 성공 여부를 기다리지 않고 바로 처리(ex. 현 실습에서의 Todo 리스트 목록 업데이트) 한 후 
        # 백엔드에서 응답이 오면 사후 검증을 진행하도록 함 -> 따라서 해당 데이터를 반환하여 비교하여 검증하도록 함
        # (이전 버전도 정상적으로 작동할 수 있게 if문을 통해 version 분기))
        if self.version >= "1.1":
            return SuccessResponseWithData(dict(id=task.id))
        else:
            return Response(data=dict(id=task.id))
    
class TaskDelete(APIView):
    def post(self, request):
        todo_id = request.data.get('todo_id')

        # todo_id에 해당하는 Task 삭제 처리
        task = Task.objects.get(id=todo_id)
        if task:
            task.delete()

        return Response(status=200)
    
class TaskToggle(APIView):
    def post(self, request):
        todo_id = request.data.get('todo_id')

        # todo_id에 해당하는 Task 완료 처리
        task = Task.objects.get(id=todo_id)
        if task:
            task.done = False if task.done is True else True
            task.save()
    
        return Response()
    
###############################################################################

################################## 샘플 코드 ##################################
# class Todo(APIView):
#     def post(self, request):
#         # == TaskCreate
#         user_id = request.data.get('user_id', "")
#         name = request.data.get('name', "")
#         end_date = request.data.get('end_date', None)
#         if end_date:
#             end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
#         Task.objects.create(user_id=user_id, name=name, end_date=end_date)

#         # == TaskSelect
#         tasks = Task.objects.all()
#         task_list = []
#         for task in tasks:
#             task_list.append(dict(name=task.name, start_date=task.start_date, end_date=task.end_date, state=task.state))
#         context = dict(task_list=task_list)
#         return render(request, 'todo/todo.html', context=context)

#     def get(self, request):
#         # == TaskSelect
#         tasks = Task.objects.all()
#         task_list = []
#         for task in tasks:
#             task_list.append(dict(name=task.name, start_date=task.start_date, end_date=task.end_date, state=task.state))
#         context=dict(task_list=task_list)
#         return render(request, 'todo/todo.html', context=context)

# # Create your views here.
# class TaskCreate(APIView):
#     def post(self, request):
#         user_id = request.data.get('user_id', "")
#         name = request.data.get('name', "")
#         end_date = request.data.get('end_date', None)
        
#         if end_date:
#             end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
#         task = Task.objects.create(user_id=user_id, name=name, end_date=end_date)

#         return Response(dict(
#             msg="To-Do 생성 완료", 
#             name=task.name, 
#             start_date=task.start_date.strftime('%Y-%m-%d'), 
#             end_date=task.end_date
#         ))

# class TaskSelect(APIView):
#     def post(self, request):
#         user_id = request.data.get('user_id', "")

#         tasks = Task.objects.filter(user_id=user_id)
#         task_list = []
#         for task in tasks:
#             task_list.append(dict(name=task.name, start_date=task.start_date, end_date=task.end_date, state=task.state))

#         return Response(dict(tasks=task_list))