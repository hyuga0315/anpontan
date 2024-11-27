from django.urls import path
from . import views

app_name = 'mychat'

urlpatterns = [
    path('',views.mainView,name='main'),
    path('createuser',views.createUser,name='createuser'),
    path('adduser',views.addUser,name='adduser'),
    path('logout',views.logout,name='logout'),
    path('room/<int:id>/',views.roomView,name='room'),
    path('createroom',views.createRoom,name='createroom'),
    path('addroom',views.addRoom,name='addroom'),
    path('search',views.searchView,name='search'),
] 
