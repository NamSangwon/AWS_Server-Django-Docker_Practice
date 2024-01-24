from rest_framework.views import APIView
from .models import Task
from rest_framework.response import Response
from datetime import datetime
from django.shortcuts import render

# Create your views here.

################################## 실습 코드 ##################################
class TaskSelect(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        page_number = request.data.get('page_number')

        # Task 조회 처리
        if user_id and not "":
            tasks = Task.objects.filter(user_id=user_id) # 해당 아이디에 해당하는 Task 조회
        else:
            tasks = Task.objects.all() # 모든 Task 조회

        # 페이징 처리 (한 페이지의 Task 수 = 10)
        is_last_page = True # 마지막 페이지 = 다음 페이지 없음
        if page_number is not None and page_number >= 0:
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

        return Response(status=200, data=dict(tasks=tasks_list, isLastPage=is_last_page))
    
class TaskCreate(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        todo_id = request.data.get('todo_id')
        name = request.data.get('name')
        
        # Task 생성
        if todo_id:
            task = Task.objects.create(id=todo_id, user_id=user_id, name=name) # 실습 2번 (id 입력 받기)
        else:
            task = Task.objects.create(user_id=user_id, name=name) # 실습 3번 (id 입력 받지 않기)

        # 사용자 편의를 위해 프론트엔드는 성공 여부를 기다리지 않고 바로 처리(ex. 현 실습에서의 Todo 리스트 목록 업데이트) 한 후 
        # 백엔드에서 응답이 오면 사후 검증을 진행하도록 함 -> 따라서 해당 데이터를 반환하여 비교하여 검증하도록 함
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