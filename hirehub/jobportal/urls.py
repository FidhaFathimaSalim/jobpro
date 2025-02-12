from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.work,name='work'),
    path('recommend_jobs/', views.recommend_jobs, name='recommend_jobs'),
    path('hirebot/', views.hirebot, name='hirebot'),
    path('cv',views. cv_create, name='cv_create'),
    path('<int:profile_id>/', views.cv_download, name='cv_download'),
    path('view/<int:profile_id>/', views.cv_view, name='cv_view'),
    path('delete/<int:profile_id>/', views.cv_delete, name='cv_delete'),
    path('update/<int:profile_id>/', views.cv_update, name='cv_update'),
    path('list', views.list_view, name='list_view'),
]