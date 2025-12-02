from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages



# View for index home page
def index(request):
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
    
    return redirect('index')

def userRegistration(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect('index')
    else:
        if request.method == "POST":
            form = UserCreationForm(request.POST)

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