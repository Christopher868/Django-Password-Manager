from django.contrib import admin
from .models import SavedAccount, UserProfile

# Register your models here.
class SavedAccountAdmin(admin.ModelAdmin):
    readonly_fields = ('user','account_title', 'encrypted_username_or_email', 'username_or_email_iv', 'encrypted_password', 'password_iv', 'created_at')

admin.site.register(SavedAccount, SavedAccountAdmin)
admin.site.register(UserProfile)
