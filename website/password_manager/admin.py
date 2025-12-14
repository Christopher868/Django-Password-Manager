from django.contrib import admin
from .models import SavedAccount, UserProfile

# Register your models here.
class SavedAccountAdmin(admin.ModelAdmin):
    readonly_fields = ('user','account_title', 'username_or_email', 'encrypted_password', 'iv', 'created_at')

admin.site.register(SavedAccount, SavedAccountAdmin)
admin.site.register(UserProfile)
