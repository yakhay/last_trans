from django.contrib import admin

# Register your models here.
# from .models import UserProfile

# admin.site.register(UserProfile)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserForm
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserForm
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('photo_profile', 'score', 'win', 'lose', 'ranking', 'total_match')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('photo_profile', 'score', 'win', 'lose', 'ranking', 'total_match')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
