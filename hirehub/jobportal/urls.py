from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.work,name='work'),
    path('recommend_jobs/', views.recommend_jobs, name='recommend_jobs'),
    path('hirebot/', views.hirebot, name='hirebot'),
    path('cv/',views. cv_create, name='cv_create'),
    path('cv/<int:profile_id>/', views.cv_download, name='cv_download'),
    path('cv/view/<int:profile_id>/', views.cv_view, name='cv_view'),
    path('cv/delete/<int:profile_id>/', views.cv_delete, name='cv_delete'),
    path('cv/update/<int:profile_id>/', views.cv_update, name='cv_update'),
    path('cv/list', views.list_view, name='list_view'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
]