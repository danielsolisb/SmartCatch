from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import User
from .forms import CustomUserChangeForm, CustomUserCreationForm
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (
            None, {
                'fields': (
                    'id_ced',
                    'address',
                    'degree_title',
                    'telephone',
                    'country',
                    'company',
                    'categorie',
                    #'StationID',
                )
            }
        ),
    )

class UserAdmin(CustomUserAdmin):
    list_display =  (
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'is_superuser',
        'id_ced',
        'address',
        'degree_title',
        'telephone',
        'country',
        'company',
        'categorie',
        'last_login',
        'date_joined',
    )



admin.site.register(User, UserAdmin)