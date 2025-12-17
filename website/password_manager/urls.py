from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_registration, name="register"),
    path('account/', views.user_account, name="user-account"),
    path('account/change-password/', views.user_change_password, name="change-password"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="accounts/password-reset-form.html"), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password-reset-done.html"), name="password_reset_done"),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password-reset-confirm.html"), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password-reset-complete.html"), name="password_reset_complete"),
    path('view-all-accounts/', views.view_all_accounts, name="view-all-accounts"),
    path('add-new-account/', views.add_account, name="add-account"),
    path('view-account/<int:account_id>/', views.view_account, name="view-account"),
    path('confirm-delete/<int:account_id>/', views.confirm_delete, name="delete-confirm"),
    path('delete/<int:account_id>/', views.delete, name="delete"),
    path('edit-saved-account/<int:account_id>/', views.edit_saved_account, name="edit-saved-account"),
    path('locked-out/', views.lockout, name='lockout'),
    path('api/retrieve-profile/', views.retrieve_user_profile, name="retrieve-profile"),
    
    
]
