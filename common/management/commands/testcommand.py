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