from django.urls import path

from . import views

# newssave应用的路由配置
urlpatterns = [
    path('newssave', views.newssave, name='newssave'),
]