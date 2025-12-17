from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm, UpdateUserForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import UserProfile, SavedAccount
from django.http import JsonResponse
from datetime import timedelta
from axes.models import AccessAttempt
from django.utils import timezone
import json
from axes.handlers.proxy import AxesProxyHandler



# View for index home page
def index(request):
    return render(request, 'index.html', {})



# View for login page
def user_login(request):
    # Checks if user is authenticated
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect('index')
    else:
        attempts_left = getattr(settings, 'AXES_FAILURE_LIMIT', 3)
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                messages.success(request, f"Login Successful. Welcome back {user.username}!")
                return redirect('index')
            else:
                messages.error(request, "Incorrect username or password!")
                # Sends remaining attempts as context to display to user
                failures = AxesProxyHandler.get_failures(request)
                attempts_left = max(0, attempts_left - failures) 
        
        return render(request, 'accounts/login.html', {'attempts_left':attempts_left}) 
    

# View for lockout page if failed login too many times
def lockout(request):  
    attempt = AccessAttempt.objects.filter(ip_address=request.META.get('REMOTE_ADDR')).latest('attempt_time')
        
    #calculating remaining time before user can login again
    unlocked_at = attempt.attempt_time + settings.AXES_COOLOFF_TIME
    now = timezone.now()
    
    seconds_remaining = int((unlocked_at - now).total_seconds())
    minutes, seconds = divmod(seconds_remaining, 60)
    time = f'{minutes}:{seconds:02d}'

    # If time is zero or below redirecting back to login
    if seconds_remaining <= 0:
        return redirect('login')
    
    return render(request, 'lockout-page.html', {'time': time})  



# View for logging out user
def user_logout(request):
    # Checks if user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, 'Must be logged in to logout')
        return redirect('login')
    else:
        logout(request)
        messages.success(request, "Successfully logged out!")
        referrer = request.META.get('HTTP_REFERER')
        return redirect(referrer)



# View for registering user
def user_registration(request):
    # Checks if user is authenticated
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect('index')
    else:
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():

                # Checks to make sure email is not already in use before continuing 
                user_email = request.POST.get('email')
                if User.objects.filter(email=user_email).exists():
                    messages.error(request, 'Account already associated with that email. Please try again.')
                    return redirect('register')
                else:
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
def user_account(request):
    # Checks if user is authenticated
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
def user_change_password(request):
    # Checks if user is authenticated
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
def view_all_accounts(request):
    # Checks if user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, "Login to view accounts!")
        return redirect('login')
    else:
        accounts = SavedAccount.objects.filter(user=request.user)
        return render(request, 'view-all-accounts.html', {'accounts':accounts})
    


# View to view saved account information
def view_account(request, account_id):
    # Checks if user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, 'Must be logged into to view saved accounts')
        return redirect('login')
    else:
        account = SavedAccount.objects.get(id=account_id)
        return render(request, 'view-account.html', {'account': account})



# View for page where users can add new saved account
def add_account(request):
    # Checks if user is authenticated
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
                username_or_email_iv = secret_data['username_or_email_iv'],
                encrypted_password = secret_data['enc_password'],
                password_iv = secret_data['password_iv'],
                encrypted_additional_data = secret_data['enc_additional_data'],
                additional_data_iv = secret_data['additional_data_iv'],
            )
            messages.success(request, "New account successfully added!")
            return redirect('view-all-accounts')

        else:
            return render(request, 'add-account.html', {})
    


# Confirms that user wants to delete a saved account
def confirm_delete(request, account_id):
    # Checks if user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, "Must be logged into the delete accounts!")
        return redirect('login')
    else:
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
    
    # Check if user is logged into an account
    if not request.user.is_authenticated:
        messages.error(request, "Must be logged into the delete accounts!")
        return redirect('login')
    else:
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
    


# View that lets user edit saved accounts
def edit_saved_account(request, account_id):
    if not request.user.is_authenticated:
        messages.error(request, "Must be logged into edit saved accounts!")
        return redirect('login')
    else:
        saved_account = get_object_or_404(SavedAccount, id=account_id)

        # Updates saved account if request method is POST
        if request.method == 'POST':
            try:
                account_title = request.POST.get('account-title')
                secret_data = json.loads(request.POST.get('secret-data'))

                # Updates saved account with new info
                saved_account.account_title = account_title

                if secret_data:
                    if 'enc_username_or_email' in secret_data:
                        saved_account.encrypted_username_or_email = secret_data['enc_username_or_email']
                
                    if 'enc_password' in secret_data:
                        saved_account.encrypted_password = secret_data['enc_password']
                
                    if 'username_or_email_iv' in secret_data:
                        saved_account.username_or_email_iv = secret_data['username_or_email_iv']
                    
                    if 'password_iv' in secret_data:
                        saved_account.password_iv = secret_data['password_iv']

                    if 'enc_additional_data' in secret_data:
                        saved_account.encrypted_additional_data = secret_data['enc_additional_data']
                    
                    if 'additional_data_iv' in secret_data:
                        saved_account.additional_data_iv = secret_data['additional_data_iv']
                    
                
                saved_account.save()
                messages.success(request, 'Account successfully updated!')
                return redirect('view-all-accounts')

            except Exception as e:
                messages.error(request, f'Error while updating account: {str(e)}')
                return redirect('view-all-accounts')

        return render(request, 'edit-saved-account.html', {'account': saved_account})


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