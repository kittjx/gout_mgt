from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .tokens import Token

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('phone', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('phone',)
    ordering = ('phone',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Token)