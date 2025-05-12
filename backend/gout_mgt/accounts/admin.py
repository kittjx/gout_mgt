from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from .models import User
from .tokens import Token

User = get_user_model()

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
    actions = ['reset_user_password']
    
    def reset_user_password(self, request, queryset):
        # Generate a random password for each selected user
        reset_count = 0
        for user in queryset:
            # Generate a random 8-character password
            new_password = get_random_string(8)
            user.set_password(new_password)
            user.save()
            self.message_user(request, f"用户 {user.phone} 的新密码是: {new_password}")
            reset_count += 1
        
        if reset_count == 1:
            message_bit = "1 个用户"
        else:
            message_bit = f"{reset_count} 个用户"
        
        self.message_user(request, f"{message_bit}的密码已重置。请记下新密码并通知用户。")
    
    reset_user_password.short_description = "重置所选用户的密码"

admin.site.register(User, CustomUserAdmin)
admin.site.register(Token)
