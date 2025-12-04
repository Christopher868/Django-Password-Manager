from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm, UpdateUserForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings



# View for index home page
def index(request):
   
    # send_mail(
    # 'Test Subject from Django',
    # 'This is the test message body.',
    # settings.DEFAULT_FROM_EMAIL, # Uses the sender address you configured
    # ['christopherhicks868@gmail.com'], # Replace with an actual recipient email
    # fail_silently=False,
    # )
    return render(request, 'index.html', {})


# View for login page
def userLogin(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect('index')
    else:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)

            if form.is_valid():
                user = form.get_user()
                login(request, user)
                messages.success(request, f"Login Successful. Welcome back {user.username}!")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password!")
        
        return render(request, 'accounts/login.html', {}) 



# View for logging out user
def userLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    referrer = request.META.get('HTTP_REFERER')
    return redirect(referrer)



# View for registering user
def userRegistration(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect('index')
    else:
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)

            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, f"Account successfully created. Welcome {user.username}!")
                return redirect('index')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

        return render(request, 'accounts/register.html', {})
    


# View for letting user edit their own information
def userAccount(request):
    if not request.user.is_authenticated:
        messages.error(request, "Must be logged into to view account information.")
        return redirect('login')
    else:
        if request.method == "POST":
            form = UpdateUserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Changes to profile saved")
                return redirect("user-account")
        else:
            form = UpdateUserForm(instance=request.user)
        return render(request, 'accounts/user-account.html', {"form":form})
    


# View for letting user change password
def userChangePassword(request):
    if not request.user.is_authenticated:
        messages.error(request, "Log in to change password!")
        return redirect('login')
    else:
        if request.method == "POST":
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password successfully changed!")
                return redirect("user-account")
        else:
            form = PasswordChangeForm(request.user)

        return render(request, 'accounts/change-pwd.html', {"form":form})