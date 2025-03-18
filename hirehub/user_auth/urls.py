from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name = "register"),
	path('login/', views.loginPage, name = "login"),  
	path('logout/', views.logoutUser, name = "logout"),
    path('cv/',views. cv_create, name='cv_create'),
    path('cv/<int:profile_id>/', views.cv_download, name='cv_download'),
    path('cv/view/<int:profile_id>/', views.cv_view, name='cv_view'),
    path('cv/delete/<int:profile_id>/', views.cv_delete, name='cv_delete'),
    path('cv/update/<int:profile_id>/', views.cv_update, name='cv_update'),
    path('cv/list', views.list_view, name='list_view'),
]
