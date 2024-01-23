from django.conf.urls import url
from . import views

urlpatterns = [
    url('select', views.TaskSelect.as_view(), name='select'),
    url('create', views.TaskCreate.as_view(), name='create'),
    url('delete', views.TaskDelete.as_view(), name='delete'),
    url('toggle', views.TaskToggle.as_view(), name='toggle')
]