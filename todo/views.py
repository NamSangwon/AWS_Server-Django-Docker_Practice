from rest_framework.views import APIView
from .models import Task
from rest_framework.response import Response
from datetime import datetime
from django.shortcuts import render

# Create your views here.

################################## 실습 코드 ##################################
class TaskSelect(APIView):
    def post(self, request):
        tasks_list = []

        # 모든 Task 가져오기
        tasks = Task.objects.all()

        for task in tasks:
            tasks_list.append(dict(id = task.id,
                                name=task.name,
                                done=task.state))

        return Response(status=200, data=dict(tasks=tasks_list))
    
class TaskCreate(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        todo_id = request.data.get('todo_id')
        name = request.data.get('name')

        # Task 생성
        Task.objects.create(id=todo_id, user_id=user_id, name=name)

        # 사용자 편의를 위해 프론트엔드는 성공 여부를 기다리지 않고 바로 처리(ex. 현 실습에서의 Todo 리스트 목록 업데이트) 한 후 
        # 백엔드에서 응답이 오면 사후 검증을 진행하도록 함 -> 따라서 해당 데이터를 반환하여 비교하여 검증하도록 함
        return Response() 
    
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