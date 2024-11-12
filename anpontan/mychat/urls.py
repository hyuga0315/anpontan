from django.urls import path
from . import views

app_name = 'mychat'

urlpatterns = [
    #ログイン認証画面
    path('', views.startView, name='start'),
    #新規ユーザ登録画面
    path('createuser', views.createUser, name='createuser'),
]