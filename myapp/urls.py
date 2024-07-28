   # file_manager/urls.py
from django.urls import re_path, path
from .views import RegisterView,FileUploadView,FileReadView,ListFilesView, ListAllFilesView

urlpatterns = [
       re_path('register/', RegisterView.as_view(), name='register'),
       re_path('files/upload/', FileUploadView.as_view(), name='file-upload'),
       path('files/read/<int:file_id>/', FileReadView.as_view(), name='file-read'),
       path('files/getall/', ListAllFilesView.as_view(), name='list-allfiles'),
       re_path('files/list/', ListFilesView.as_view(), name='file-list'),
   ]