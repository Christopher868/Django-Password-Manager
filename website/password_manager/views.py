from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm, UpdateUserForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import UserProfile, SavedAccount
from django.http import JsonResponse
import json


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
                messages.error(request, "Incorrect username or password!")
        
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
                # Saves user in database and logs them in
                user = form.save()
                login(request, user)


                # Creates profile for user for encryption and decryption
                profileData = json.loads(request.POST.get('profile-data'))
                UserProfile.objects.create(
                    user=user,
                    salt = profileData['salt'],
                    iterations = profileData['iterations'],
                    iv = profileData['validation_iv'],
                    cipher_text = profileData['validation_ciphertext']
                )
                

                messages.success(request, f"Account successfully created. Welcome {user.username}!")
                return redirect('index')
            else:
                # Displays form errors to users
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

        return render(request, 'accounts/register.html', {})
    


# View for letting user edit their own account information once logged in
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
                # Displays form errors to users
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{error}")
        else:
            form = UpdateUserForm(instance=request.user)
        return render(request, 'accounts/user-account.html', {"form":form})
    


# View for letting user change password
def userChangePassword(request):
    if not request.user.is_authenticated:
        messages.error(request, "Login to change password!")
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
                # Displays form errors to users
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{error}")
        else:
            form = PasswordChangeForm(request.user)

        return render(request, 'accounts/change-pwd.html', {"form":form})
    

# View for page where users can view their saved accounts
def viewAllAccounts(request):
    if not request.user.is_authenticated:
        messages.error(request, "Login to view accounts!")
        return redirect('login')
    else:
        accounts = SavedAccount.objects.filter(user=request.user)
        return render(request, 'view-all-accounts.html', {'accounts':accounts})
    
# View to view saved account information
def viewAccount(request, account_id):
    account = SavedAccount.objects.get(id=account_id)
    return render(request, 'view-account.html', {'account': account})


# View for page where users can add new saved account
def addAccount(request):
    if not request.user.is_authenticated:
        messages.error(request, "Login to add new saved account!")
        return redirect('login')
    else:
        if request.method == "POST":
            account_title = request.POST.get('account-title')
            secret_data = json.loads(request.POST.get('secret-data'))

            # Creates saved account
            SavedAccount.objects.create(
                user=request.user,
                account_title = account_title,
                encrypted_username_or_email = secret_data['enc_username_or_email'],
                encrypted_password = secret_data['enc_password'],
                iv = secret_data['validation_iv'],
            )
            messages.success(request, "New account successfully added!")
            return redirect('view-all-accounts')

        else:
            return render(request, 'add-account.html', {})
    

# Confirms that user wants to delete a saved account
def confirmDelete(request, account_id):
    referer_url = request.META.get('HTTP_REFERER')

    # Makes http referer is from view-all-accounts page and redirects if it is not 
    if referer_url is None or not referer_url.endswith('view-all-accounts/'):
        messages.error(request, 'Accounts must be deleted from the saved accounts page')
        return redirect('view-all-accounts')
    else:
        savedAccount = SavedAccount.objects.get(id=account_id)
        return render(request, 'delete-confirm.html', {'account':savedAccount})



# Deletes user's selected saved account
def delete(request, account_id):
    # Checks to make sure page is being accessed from confirm delete page
    referer_url = request.META.get('HTTP_REFERER')
    if referer_url is not None:
        referer_url = referer_url.split('/')
        referer_url = referer_url[3]
    
    # Sends error msg and redirects to view-all-accounts if http referer is not from confirm delete
    if referer_url is None or referer_url != 'confirm-delete':
        messages.error(request, 'Accounts must be deleted from the saved accounts page')
        return redirect('view-all-accounts')
    else:
        savedAccount = SavedAccount.objects.get(id=account_id)
        savedAccount.delete()
        messages.success(request, 'Account deleted Successfully!')
    return redirect('view-all-accounts')


# Api endpoint for retrieving user profile
def retrieve_user_profile(request):
    if not request.user.is_authenticated:  
       return JsonResponse({'error': 'Login required'}, status=401)
    else:
        if request.method == 'GET':
            profile = request.user.userprofile
            data = {
                'salt': profile.salt,
                'iterations': profile.iterations,
                'iv': profile.iv,
                'cipher_text': profile.cipher_text,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Only GET requested allowed'}, status=405)