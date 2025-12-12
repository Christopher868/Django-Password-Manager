from django.contrib import admin
from .models import SavedAccount

# Register your models here.
class SavedAccountAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'encrypted_username_or_email', 'encrypted_password', 'key_salt', 'iv', 'created_at')
admin.site.register(SavedAccount, )