from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('register/', views.userRegistration, name="register"),
    path('account/', views.userAccount, name="user-account"),
    path('account/change-password/', views.userChangePassword, name="change-password"),
]
