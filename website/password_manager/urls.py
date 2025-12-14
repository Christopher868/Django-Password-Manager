from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('register/', views.userRegistration, name="register"),
    path('account/', views.userAccount, name="user-account"),
    path('account/change-password/', views.userChangePassword, name="change-password"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="accounts/password-reset-form.html"), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password-reset-done.html"), name="password_reset_done"),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password-reset-confirm.html"), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password-reset-complete.html"), name="password_reset_complete"),
    path('view-all-accounts/', views.viewAllAccounts, name="view-all-accounts"),
    path('add-new-account/', views.addAccount, name="add-account"),
    path('view-account/<int:account_id>/', views.viewAccount, name="view-account"),
    path('api/retrieve-profile/', views.retrieve_user_profile, name="retrieve-profile"),
    
]
